import pandas as pd
import math
from src.co2_calculator.structures.wall_base import BaseWall

# for debugging
# from wall_base import wall_base

filename_database = './src/co2_calculator/documents/CO2-eq Fußabdruck - Vergleich Allgemein_bara.xlsx'

class MIPWall(BaseWall):
    """ Concrete class for pile walls"""
    def __init__(self, wall_area=3430.0, wall_thickness=0.55, productivity=250.0, cement=100.0, betonite=20.0, 
                diesel=750.0, electricity=80.0, excess=35.0):
        super().__init__()
        self.wall_area = wall_area                          # m^2
        self.wall_thickness = wall_thickness                # m
        self.productivity = productivity                    # m^2/AT
        self.cement = cement                                # kg/m^3
        self.betonite = betonite                            # kg/m^3
        self.diesel = diesel                                # liter/AT
        self.electricity = electricity                      # kWh/h
        self.excess = excess                                # Rückfluss/ Bohrüberschuss (von Wandvolumen abgeschätzt)
        self.weight_steelprofile = 0.0                      # This wall has no stell reinforcement

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
        df = pd.read_excel(filename_database, sheet_name='Calculations MIP-DW', usecols=columns, names=names)
        df = df.fillna(0.0)
        return df


    def get_material_production(self):
        """ Gets tCO2_eq by the production of material
        """
        df = self.df['K']
        vK_cement =      float(df.iloc[18])
        vK_steel =       float(df.iloc[19])
        vK_betonite =    float(df.iloc[20])
        tCO2eq = 0.0
        tCO2eq += vK_cement*self.wall_area*self.cement/1000*self.wall_thickness
        tCO2eq += vK_steel*self.weight_steelprofile
        tCO2eq += vK_betonite*self.wall_area*self.betonite/1000*self.wall_thickness
        return tCO2eq


    def get_material_transport(self):
        """ Gets tCO2_eq by the transport of material
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_cement =          float(df.iloc[51])
            v_steel =           float(df.iloc[52])
            v_betonite =        float(df.iloc[53])
            v_diesel =          float(df.iloc[54])
            return (v_cement, v_steel, v_betonite, v_diesel)

        def get_transport_times(G,I):
            """ gets transport times, column M"""
            return math.ceil(G/I)

        vI_cement, vI_steel, vI_betonite, vI_diesel = get_column_values(column='I')
        vJ_cement, vJ_steel, vJ_betonite, vJ_diesel = get_column_values(column='J')
        vK_cement, vK_steel, vK_betonite, vK_diesel = get_column_values(column='K')
        vO_cement, vO_steel, vO_betonite, vO_diesel = get_column_values(column='O')
        weight_cement = self.wall_area*self.cement/1000*self.wall_thickness
        weight_betonite = self.wall_area*self.betonite/1000*self.wall_thickness
        working_days = self.wall_area/self.productivity
        diesel_consumption = self.diesel*working_days
        tCO2eq = 0.0
        tCO2eq += vJ_cement*get_transport_times(weight_cement, vI_cement)*vK_cement*(1.0+vO_cement/100)
        tCO2eq += vJ_steel*get_transport_times(self.weight_steelprofile, vI_steel)*vK_steel*(1.0+vO_steel/100)
        tCO2eq += vJ_betonite*get_transport_times(weight_betonite, vI_betonite)*vK_betonite*(1.0+vO_betonite/100)
        tCO2eq += vJ_diesel*get_transport_times(diesel_consumption, vI_diesel)*vK_diesel*(1.0+vO_diesel/100)
        return tCO2eq


    def get_disposal_transport(self):
        """ Gets tCO2_eq by disposal transport
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_bohrgut =          float(df.iloc[94])
            v_schlamm =           float(df.iloc[95])
            v_suspension =        float(df.iloc[96])
            return (v_bohrgut, v_schlamm, v_suspension)

        def get_transport_times(G,I):
            """ gets transport times, column M"""
            return math.ceil(G/I)
        
        weight_transport_bohrgut = 2*self.wall_area*self.wall_thickness*self.excess/100
        _, weight_transport_schlamm, weight_transport_suspension = get_column_values(column='C')
        vK_bohrgut, vK_schlamm, vK_suspension = get_column_values(column='K')
        vI_bohrgut, vI_schlamm, vI_suspension = get_column_values(column='I')
        vJ_bohrgut, vJ_schlamm, vJ_suspension = get_column_values(column='J')
        vO_bohrgut, vO_schlamm, vO_suspension = get_column_values(column='O')
        tCO2eq = 0.0
        tCO2eq += get_transport_times(weight_transport_bohrgut, vI_bohrgut)*vJ_bohrgut*vK_bohrgut*(1.0 + vO_bohrgut/100)
        tCO2eq += get_transport_times(weight_transport_schlamm, vI_schlamm)*vJ_schlamm*vK_schlamm*(1.0 + vO_schlamm/100)
        tCO2eq += get_transport_times(weight_transport_suspension, vI_suspension)*vJ_suspension*vK_suspension*(1.0 + vO_suspension/100)
        return tCO2eq


    def get_equipment(self):
        """ Gets tCO2_eq by equipment
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_RG25 =                    float(df.iloc[126])
            v_site_setup =              float(df.iloc[127])
            v_mixer_silo_pump =         float(df.iloc[128])
            v_excavator =               float(df.iloc[129])
            v_0 =                       float(df.iloc[130])
            v_ramme =                   float(df.iloc[131])
            v_Hitachi =                 float(df.iloc[132])
            return (v_RG25, v_site_setup, v_mixer_silo_pump, v_excavator, v_0, v_ramme, v_Hitachi)

        working_days = self.wall_area/self.productivity
        vC_RG25, vC_site_setup, vC_mixer_silo_pump, vC_excavator, vC_0, vC_ramme, vC_Hitachi = get_column_values(column='C')
        vG_RG25, vG_site_setup, vG_mixer_silo_pump, vG_excavator, vG_0, vG_ramme, vG_Hitachi = get_column_values(column='G')
        vH_RG25, vH_site_setup, vH_mixer_silo_pump, vH_excavator, vH_0, vH_ramme, vH_Hitachi = get_column_values(column='H')
        vI_RG25, vI_site_setup, vI_mixer_silo_pump, vI_excavator, vI_0, vI_ramme, vI_Hitachi = get_column_values(column='I')
        tCO2eq = 0.0
        tCO2eq += vC_RG25*(working_days/vH_RG25)/vG_RG25*vI_RG25
        tCO2eq += vC_site_setup*(working_days/vH_site_setup)/vG_site_setup*vI_site_setup
        tCO2eq += vC_mixer_silo_pump*(working_days/vH_mixer_silo_pump)/vG_mixer_silo_pump*vI_mixer_silo_pump
        tCO2eq += vC_excavator*(working_days/vH_excavator)/vG_excavator*vI_excavator
        tCO2eq += vC_0*(0.0/vH_0)/vG_0*vI_0
        tCO2eq += vC_ramme*(working_days/vH_ramme)/vG_ramme*vI_ramme
        tCO2eq += vC_Hitachi*(working_days/vH_Hitachi)/vG_Hitachi*vI_Hitachi
        return tCO2eq


    def get_energy_electricity_hour(self):
        """ Gets tCO2_eq by energy electricity hour
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_diesel =          float(df.iloc[163])
            v_electricity =     float(df.iloc[166])
            return (v_diesel, v_electricity)

        working_days = self.wall_area/self.productivity
        diesel_consumption = self.diesel*working_days
        electricity_consumption = self.electricity*10.0*working_days
        vK_diesel, vK_electricity = get_column_values(column='K')
        tCO2eq = 0.0
        tCO2eq += diesel_consumption*vK_diesel/1000
        tCO2eq += electricity_consumption*vK_electricity/1000
        return tCO2eq


    def get_mob_demob(self):
        """ Gets tCO2_eq by mobilization and demobilization
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_RG25 =                    float(df.iloc[195])
            v_mixer_silo_pump =         float(df.iloc[196])
            v_BE =                      float(df.iloc[197])
            v_0 =                       float(df.iloc[198])
            v_ramme =                   float(df.iloc[199])
            v_Hitachi =                 float(df.iloc[200])
            return (v_RG25, v_mixer_silo_pump, v_BE, v_0, v_ramme, v_Hitachi)

        vF_RG25, vF_mixer_silo_pump, vF_BE, vF_0, vF_ramme, vF_Hitachi = get_column_values(column='F')
        vG_RG25, vG_mixer_silo_pump, vG_BE, vG_0, vG_ramme, vG_Hitachi = get_column_values(column='G')
        vK_RG25, vK_mixer_silo_pump, vK_BE, vK_0, vK_ramme, vK_Hitachi = get_column_values(column='K')
        tCO2eq = 0.0
        tCO2eq += self.distance_mob_demob*vF_RG25*vG_RG25*vK_RG25
        tCO2eq += self.distance_mob_demob*vF_mixer_silo_pump*vG_mixer_silo_pump*vK_mixer_silo_pump
        tCO2eq += self.distance_mob_demob*vF_BE*vG_BE*vK_BE
        tCO2eq += self.distance_mob_demob*vF_0*vG_0*vK_0
        tCO2eq += self.distance_mob_demob*vF_ramme*vG_ramme*vK_ramme
        tCO2eq += self.distance_mob_demob*vF_Hitachi*vG_Hitachi*vK_Hitachi
        return tCO2eq


    def get_persons_transport(self):
        """ Gets tCO2_eq by transport of persons
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v = float(df.iloc[220])
            return v

        v_G = get_column_values(column='G')
        v_H = get_column_values(column='H')
        v_I = get_column_values(column='I')
        v_K = get_column_values(column='K')
        working_days = self.wall_area/self.productivity
        tCO2eq = 0.0
        tCO2eq += 2*working_days*v_I*v_G/v_H * v_K
        return tCO2eq


    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        """
        self.out_material_production = self.get_material_production()
        self.out_material_transport = self.get_material_transport()
        self.out_disposal_transport = self.get_disposal_transport()
        self.out_equipment = self.get_equipment()
        self.out_energy_electricity_hour = self.get_energy_electricity_hour()
        self.out_mob_demob = self.get_mob_demob()
        self.out_persons_transport = self.get_persons_transport()

        return sum([self.out_material_production, self.out_material_transport, self.out_disposal_transport, self.out_equipment,
                    self.out_energy_electricity_hour, self.out_mob_demob, self.out_persons_transport])

#if __name__ == '__main__':
#    wall = PileWall()
#    print(dir(wall))
#    print(wall.borelength_lfm)
#    print(issubclass(PileWall, BaseWall))
#    print(isinstance(wall, BaseWall))
#    print(PileWall.__mro__)