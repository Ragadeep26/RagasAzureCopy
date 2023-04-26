from random import randint
#from src.file_utilitites import read_excel
import pandas as pd
import math
import streamlit as st

filename_database = './src/co2_calculator/documents/CO2-eq Fußabdruck - Vergleich Allgemein_bara.xlsx'

class Anchor(object):
    """ Class for anchor"""
    def __init__(self, project_name='Sample Project', anchor_lfm=2906.0, weight_anchorhead=10.0, weight_anchorstrands=10.0, productivity=100.0,
                cement=25.0, diesel=200.0, electricity=16.0, distance_mob_demob=250.0):
        self.id = randint(10000, 99999)
        self.project_name = project_name                    # used for referencing to which project the structure belongs to
        self.anchor_lfm = anchor_lfm                        # m
        self.weight_anchorhead = weight_anchorhead          # ton
        self.weight_anchorstrands = weight_anchorstrands    # ton
        self.productivity = productivity                    # Leistung, m/AT (Meter pro Arbeitstag)
        self.cement = cement                                # Zementeinsatz, kg/m
        self.diesel = diesel                                # liter/AT
        self.electricity = electricity                      # kWh/h
        self.distance_mob_demob = distance_mob_demob        # km

        # dataframe (read from excel)
        self.df = self.read_database(columns='C,F,G,H,I,J,K,M,O', names=['C', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'O'])

        # outputs
        self.out_material_production = 0.0                      # tCO2_eq
        self.out_material_transport = 0.0                       # tCO2_eq
        self.out_disposal_transport = 0.0                       # tCO2_eq
        self.out_equipment = 0.0                                # tCO2_eq
        self.out_energy_electricity_hour = 0.0                  # tCO2_eq
        self.out_mob_demob = 0.0                                # tCO2_eq
        self.out_persons_transport = 0.0                        # tCO2_eq


    def read_database(self, columns='C', names=['C']):
        """ Reads parameter stored in Excel database
        Note: time consuming!!
        """
        df = pd.read_excel(filename_database, sheet_name='Calculations Anker', usecols=columns, names=names)
        df = df.fillna(0.0)
        return df


    def get_material_production(self):
        """ Gets tCO2_eq by the production of material
        """
        df = self.df['K']
        param_anchorhead =      float(df.iloc[19])
        param_anchorstrand =    float(df.iloc[20])
        param_cement =          float(df.iloc[21])
        weight_cement = self.anchor_lfm * self.cement/1000.0 # cement weight [ton]
        tCO2eq = self.weight_anchorhead*param_anchorhead + self.weight_anchorstrands*param_anchorstrand + weight_cement*param_cement
        return tCO2eq


    def get_material_transport(self):
        """ Gets tCO2_eq by the transport of material
        """
        def get_transport_times():
            """ gets transport times, column M"""
            df_I = self.df['I']
            transport_times_anchorhead = (self.weight_anchorhead + self.weight_anchorstrands)/float(df_I.iloc[55])
            transport_times_cement = self.anchor_lfm * self.cement/1000/float(df_I.iloc[56])
            working_days = self.anchor_lfm/self.productivity
            diesel_consumption = working_days*self.diesel
            transport_times_diesel = diesel_consumption/float(df_I.iloc[58])
            return (math.ceil(transport_times_anchorhead), math.ceil(transport_times_cement), math.ceil(transport_times_diesel))

        transport_times_anchorhead, transport_times_cement, transport_times_diesel = get_transport_times()
        #print(transport_times_anchorhead, transport_times_cement, transport_times_diesel)
        df_J, df_K, df_O = self.df['J'], self.df['K'], self.df['O']
        param_J_anchorhead =      float(df_J.iloc[55])
        param_J_cement =          float(df_J.iloc[56])
        param_J_diesel =          float(df_J.iloc[58])
        param_K_anchorhead =      float(df_K.iloc[55])
        param_K_cement =          float(df_K.iloc[56])
        param_K_diesel =          float(df_K.iloc[58])
        param_O_anchorhead =      float(df_O.iloc[55])
        param_O_cement =          float(df_O.iloc[56])
        param_O_diesel =          float(df_O.iloc[58])
        tCO2eq = 0.0
        tCO2eq += transport_times_anchorhead * param_J_anchorhead * param_K_anchorhead * (1.0 + param_O_anchorhead/100)
        tCO2eq += transport_times_cement * param_J_cement * param_K_cement * (1.0 + param_O_cement/100)
        tCO2eq += transport_times_diesel * param_J_diesel * param_K_diesel * (1.0 + param_O_diesel/100)
        return tCO2eq


    def get_disposal_transport(self):
        """ Gets tCO2_eq by disposal transport
        """
        def get_transport_times():
            """ gets transport times, column M"""
            df_I, df_G = self.df['I'], self.df['G']
            transport_times_bohrgut =       float(df_G.iloc[98])/ float(df_I.iloc[98])
            transport_times_schlamm =       float(df_G.iloc[99])/ float(df_I.iloc[99])
            transport_times_suspension =    float(df_G.iloc[100])/float(df_I.iloc[100])
            return (math.ceil(transport_times_bohrgut), math.ceil(transport_times_schlamm), math.ceil(transport_times_suspension))

        transport_times_bohrgut, transport_times_schlamm, transport_times_suspension = get_transport_times()
        #print(transport_times_bohrgut, transport_times_schlamm, transport_times_suspension)
        df_J, df_K, df_O = self.df['J'], self.df['K'], self.df['O']
        param_J_anchorhead =      float(df_J.iloc[98])
        param_J_cement =          float(df_J.iloc[99])
        param_J_diesel =          float(df_J.iloc[100])
        param_K_anchorhead =      float(df_K.iloc[98])
        param_K_cement =          float(df_K.iloc[99])
        param_K_diesel =          float(df_K.iloc[100])
        param_O_anchorhead =      float(df_O.iloc[98])
        param_O_cement =          float(df_O.iloc[99])
        param_O_diesel =          float(df_O.iloc[100])
        tCO2eq = 0.0
        tCO2eq += transport_times_bohrgut * param_J_anchorhead * param_K_anchorhead * (1.0 + param_O_anchorhead/100)
        tCO2eq += transport_times_schlamm * param_J_cement * param_K_cement * (1.0 + param_O_cement/100)
        tCO2eq += transport_times_suspension * param_J_diesel * param_K_diesel * (1.0 + param_O_diesel/100)
        return tCO2eq


    def get_equipment(self):
        """ Gets tCO2_eq by equipment
        """
        def get_column_values(column='C'):
            """ gets values from column"""
            df = self.df[column]
            v_site_setup =          float(df.iloc[131])
            v_mixer_silo_pump =     float(df.iloc[132])
            v_excavator =           float(df.iloc[133])
            v_KR806 =               float(df.iloc[134])
            v_unknown1 =            0.0
            v_unknown2 =            0.0
            v_unknown3 =            0.0
            if column is not 'C':
                v_unknown1 =        float(df.iloc[130])
                v_unknown2 =        float(df.iloc[135])
                v_unknown3 =        float(df.iloc[136])
            return (v_unknown1, v_site_setup, v_mixer_silo_pump, v_excavator, v_KR806, v_unknown2, v_unknown3)
        
        working_days = self.anchor_lfm/self.productivity
        vC_unknown1, vC_site_setup, vC_mixer_silo_pump, vC_excavator, vC_KR806, vC_unknown2, vC_unknown3 = get_column_values(column='C')
        vG_unknown1, vG_site_setup, vG_mixer_silo_pump, vG_excavator, vG_KR806, vG_unknown2, vG_unknown3 = get_column_values(column='G')
        vH_unknown1, vH_site_setup, vH_mixer_silo_pump, vH_excavator, vH_KR806, vH_unknown2, vH_unknown3 = get_column_values(column='H')
        vI_unknown1, vI_site_setup, vI_mixer_silo_pump, vI_excavator, vI_KR806, vI_unknown2, vI_unknown3 = get_column_values(column='I')
        tCO2eq = 0.0
        tCO2eq += vC_unknown1*(working_days/vH_unknown1)/vG_unknown1*vI_unknown1
        tCO2eq += vC_site_setup*(working_days/vH_site_setup)/vG_site_setup*vI_site_setup
        tCO2eq += vC_mixer_silo_pump*(working_days/vH_mixer_silo_pump)/vG_mixer_silo_pump*vI_mixer_silo_pump
        tCO2eq += vC_excavator*(working_days/vH_excavator)/vG_excavator*vI_excavator
        tCO2eq += vC_KR806*(working_days/vH_KR806)/vG_KR806*vI_KR806
        tCO2eq += vC_unknown2*(working_days/vH_unknown2)/vG_unknown2*vI_unknown2
        tCO2eq += vC_unknown3*(working_days/vH_unknown3)/vG_unknown3*vI_unknown3
        return tCO2eq


    def get_energy_electricity_hour(self):
        """ Gets tCO2_eq by energy electricity hour
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_diesel =          float(df.iloc[167])
            v_electricity =     float(df.iloc[170])
            return (v_diesel, v_electricity)

        vK_diesel, vK_electricity = get_column_values(column='K')
        tCO2eq = 0.0
        tCO2eq += self.diesel*vK_diesel/1000
        working_days = self.anchor_lfm/self.productivity
        tCO2eq += self.electricity*working_days*10*vK_electricity/1000
        return tCO2eq


    def get_mob_demob(self):
        """ Gets tCO2_eq by mobilization and demobilization
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_unknown1 =                float(df.iloc[199])
            v_mixer_silo_pump =         float(df.iloc[200])
            v_BE =                      float(df.iloc[201])
            v_KR806 =                   float(df.iloc[202])
            v_unknown2 =                float(df.iloc[203])
            v_unknown3 =                float(df.iloc[204])
            return (v_unknown1, v_mixer_silo_pump, v_BE, v_KR806, v_unknown2, v_unknown3)
        
        vF_unknown1, vF_mixer_silo_pump, vF_BE, vF_KR806, vF_unknown2, vF_unknown3 = get_column_values(column='F')
        vG_unknown1, vG_mixer_silo_pump, vG_BE, vG_KR806, vG_unknown2, vG_unknown3 = get_column_values(column='G')
        vK_unknown1, vK_mixer_silo_pump, vK_BE, vK_KR806, vK_unknown2, vK_unknown3 = get_column_values(column='K')
        tCO2eq = 0.0
        tCO2eq += self.distance_mob_demob*vF_unknown1*vG_unknown1*vK_unknown1
        tCO2eq += self.distance_mob_demob*vF_mixer_silo_pump*vG_mixer_silo_pump*vK_mixer_silo_pump
        tCO2eq += self.distance_mob_demob*vF_BE*vG_BE*vK_BE
        tCO2eq += self.distance_mob_demob*vF_KR806*vG_KR806*vK_KR806
        tCO2eq += self.distance_mob_demob*vF_unknown2*vG_unknown2*vK_unknown2
        tCO2eq += self.distance_mob_demob*vF_unknown3*vG_unknown3*vK_unknown3
        return tCO2eq


    def get_persons_transport(self):
        """ Gets tCO2_eq by transport of persons
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v = float(df.iloc[224])
            return v

        v_G = get_column_values(column='G')
        v_H = get_column_values(column='H')
        v_I = get_column_values(column='I')
        v_K = get_column_values(column='K')
        working_days = self.anchor_lfm/self.productivity
        tCO2eq = 0.0
        tCO2eq += 2*working_days*v_I*v_G/v_H * v_K
        return tCO2eq


    @st.cache(suppress_st_warning=True)
    def calc_co2eq(self, **kwargs):
        """ Calculates equivalent CO2 emission tCO2eq
        """
        #self.__dict__.update(kwargs)    # update atrributes
        #print("Cache miss: expensive_computation!")

        self.out_material_production = self.get_material_production()
        self.out_material_transport = self.get_material_transport()
        self.out_disposal_transport = self.get_disposal_transport()
        self.out_equipment = self.get_equipment()
        self.out_energy_electricity_hour = self.get_energy_electricity_hour()
        self.out_mob_demob = self.get_mob_demob()
        self.out_persons_transport = self.get_persons_transport()

        return sum([self.out_material_production, self.out_material_transport, self.out_disposal_transport, self.out_equipment,
                    self.out_energy_electricity_hour, self.out_mob_demob, self.out_persons_transport])

        # for debugging
        #df = self.get_mob_demob()
        #return df

