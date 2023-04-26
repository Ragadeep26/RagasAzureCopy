import pandas as pd
import math
from src.co2_calculator.structures.wall_base import BaseWall

# for debugging
# from wall_base import wall_base

filename_database = './src/co2_calculator/documents/CO2-eq Fußabdruck - Vergleich Allgemein_bara.xlsx'

class PileWall(BaseWall):
    """ Concrete class for pile walls"""
    def __init__(self, borelength_lfm=5000.0, length_drilling_template=300.0, volume_concrete={'C16/20': 1000.0, 'C20/25': 1100.0, 'C25/30': 1200.0, 'C30/37': 1300.0, 'C35/45': 1400.0, 'C40/50': 700.0}, 
                weight_reinf_steel=270.0, weight_soil_disposal=9000.0):
        super().__init__()
        self.borelength_lfm = borelength_lfm                        # m
        self.length_drilling_template = length_drilling_template    # Bohrschablone Länge, m
        self.volume_concrete = volume_concrete
        self.weight_reinf_steel = weight_reinf_steel                # reinforcement steel in ton
        self.weight_soil_disposal = weight_soil_disposal            # Bohrgut, to be clarified?

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
        df = pd.read_excel(filename_database, sheet_name='Calculation Pfähle', usecols=columns, names=names)
        df = df.fillna(0.0)
        return df


    def get_material_production(self):
        """ Gets tCO2_eq by the production of material
        """
        df = self.df['K']
        vK_C16 =        float(df.iloc[3])
        vK_C20 =        float(df.iloc[4])
        vK_C25 =        float(df.iloc[5])
        vK_C30 =        float(df.iloc[6])
        vK_C35 =        float(df.iloc[7])
        vK_C40 =        float(df.iloc[8])
        vK_bohrschablone =  float(df.iloc[9])
        vK_reinf_steel =    float(df.iloc[10])
        tCO2eq = 0.0
        tCO2eq += vK_C16*self.volume_concrete['C16/20']
        tCO2eq += vK_C20*self.volume_concrete['C20/25']
        tCO2eq += vK_C25*self.volume_concrete['C25/30']
        tCO2eq += vK_C30*self.volume_concrete['C30/37']
        tCO2eq += vK_C35*self.volume_concrete['C35/45']
        tCO2eq += vK_C40*self.volume_concrete['C40/50']
        tCO2eq += vK_bohrschablone*self.length_drilling_template*0.4
        tCO2eq_material_tranport = float(tCO2eq)                        # to be used as argument in get_material_transport
        tCO2eq += vK_reinf_steel*self.weight_reinf_steel
        return tCO2eq, tCO2eq_material_tranport


    def get_material_transport(self, tCO2eq_material_tranport):
        """ Gets tCO2_eq by the transport of material
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_concrete =            float(df.iloc[44])
            v_reinf_steel =         float(df.iloc[45])
            v_diesel =              float(df.iloc[48])
            return (v_concrete, v_reinf_steel, v_diesel)

        def get_transport_times(G,I):
            """ gets transport times, column M"""
            return math.ceil(G/I)

        vI_concrete, vI_reinf_steel, vI_diesel = get_column_values(column='I')
        vJ_concrete, vJ_reinf_steel, vJ_diesel = get_column_values(column='J')
        vK_concrete, vK_reinf_steel, vK_diesel = get_column_values(column='K')
        vO_concrete, vO_reinf_steel, vO_diesel = get_column_values(column='O')
        concrete_volume = sum(list(self.volume_concrete.values()))
        concrete_volume += self.length_drilling_template*0.4
        working_days = self.borelength_lfm/self.productivity
        liter_diesel = self.diesel*working_days
        tCO2eq = 0.0
        tCO2eq += vJ_concrete*get_transport_times(concrete_volume, vI_concrete)*vK_concrete*(1.0+vO_concrete/100)
        tCO2eq += vJ_reinf_steel*get_transport_times(self.weight_reinf_steel, vI_reinf_steel)*vK_reinf_steel*(1.0+vO_reinf_steel/100)
        tCO2eq += vJ_diesel*get_transport_times(liter_diesel, vI_diesel)*vK_diesel*(1.0+vO_diesel/100)
        return (tCO2eq + 0.07*tCO2eq_material_tranport)


    def get_disposal_transport(self):
        """ Gets tCO2_eq by disposal transport
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_aushub =          float(df.iloc[98])
            v_schlamm =         float(df.iloc[99])
            v_bohrgut =         float(df.iloc[100])
            return (v_aushub, v_schlamm, v_bohrgut)

        def get_transport_times(G,I):
            """ gets transport times, column M"""
            return math.ceil(G/I)
        vI_aushub, vI_schlamm, vI_bohrgut = get_column_values(column='I')
        vK_aushub, vK_schlamm, vK_bohrgut = get_column_values(column='K')
        vJ_aushub, vJ_schlamm, vJ_bohrgut = get_column_values(column='J')
        vO_aushub, vO_schlamm, vO_bohrgut = get_column_values(column='O')
        tCO2eq = 0.0
        tCO2eq += get_transport_times(0.0, vI_aushub)*vJ_aushub*vK_aushub*(1.0 + vO_aushub/100)
        tCO2eq += get_transport_times(0.0, vI_schlamm)*vJ_schlamm*vK_schlamm*(1.0 + vO_schlamm/100)
        tCO2eq += get_transport_times(self.weight_soil_disposal, vI_bohrgut)*vJ_bohrgut*vK_bohrgut*(1.0 + vO_bohrgut/100)
        return tCO2eq


    def get_equipment(self):
        """ Gets tCO2_eq by equipment
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_BG39 =                    float(df.iloc[122])
            v_site_setup =              float(df.iloc[123])
            v_bohrmachine =             float(df.iloc[124])
            v_excavator =               float(df.iloc[125])
            v_Hitachi =                 float(df.iloc[126])
            v_crane =                   float(df.iloc[127])
            return (v_BG39, v_site_setup, v_bohrmachine, v_excavator, v_Hitachi, v_crane)

        working_days = self.borelength_lfm/self.productivity
        vC_BG39, vC_site_setup, vC_bohrmachine, vC_excavator, vC_Hitachi, vC_crane = get_column_values(column='C')
        vG_BG39, vG_site_setup, vG_bohrmachine, vG_excavator, vG_Hitachi, vG_crane = get_column_values(column='G')
        vH_BG39, vH_site_setup, vH_bohrmachine, vH_excavator, vH_Hitachi, vH_crane = get_column_values(column='H')
        vI_BG39, vI_site_setup, vI_bohrmachine, vI_excavator, vI_Hitachi, vI_crane = get_column_values(column='I')
        tCO2eq = 0.0
        tCO2eq += vC_BG39*(working_days/vH_BG39)/vG_BG39*vI_BG39
        tCO2eq += vC_site_setup*(working_days/vH_site_setup)/vG_site_setup*vI_site_setup
        tCO2eq += vC_bohrmachine*(working_days/vH_bohrmachine)/vG_bohrmachine*vI_bohrmachine
        tCO2eq += vC_excavator*(working_days/vH_excavator)/vG_excavator*vI_excavator
        tCO2eq += vC_Hitachi*(working_days/vH_Hitachi)/vG_Hitachi*vI_Hitachi
        tCO2eq += vC_crane*(working_days/vH_crane)/vG_crane*vI_crane
        return tCO2eq


    def get_energy_electricity_hour(self):
        """ Gets tCO2_eq by energy electricity hour
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_diesel =          float(df.iloc[162])
            v_electricity =     float(df.iloc[165])
            return (v_diesel, v_electricity)

        working_days = self.borelength_lfm/self.productivity
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
            v_BG39 =                    float(df.iloc[194])
            v_crane =                   float(df.iloc[195])
            v_BE =                      float(df.iloc[196])
            v_bohrmachine =             float(df.iloc[197])
            v_Hitachi =                 float(df.iloc[198])
            return (v_BG39, v_crane, v_BE, v_bohrmachine, v_Hitachi, v_crane)
    
        vF_BG39, vF_crane, vF_BE, vF_bohrmachine, vF_Hitachi, vF_crane = get_column_values(column='F')
        vG_BG39, vG_crane, vG_BE, vG_bohrmachine, vG_Hitachi, vG_crane = get_column_values(column='G')
        vK_BG39, vK_crane, vK_BE, vK_bohrmachine, vK_Hitachi, vK_crane = get_column_values(column='K')
        tCO2eq = 0.0
        tCO2eq += self.distance_mob_demob*vF_BG39*vG_BG39*vK_BG39
        tCO2eq += self.distance_mob_demob*vF_crane*vG_crane*vK_crane
        tCO2eq += self.distance_mob_demob*vF_BE*vG_BE*vK_BE
        tCO2eq += self.distance_mob_demob*vF_bohrmachine*vG_bohrmachine*vK_bohrmachine
        tCO2eq += self.distance_mob_demob*vF_Hitachi*vG_Hitachi*vK_Hitachi
        return tCO2eq


    def get_persons_transport(self):
        """ Gets tCO2_eq by transport of persons
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v = float(df.iloc[225])
            return v

        v_G = get_column_values(column='G')
        v_H = get_column_values(column='H')
        v_I = get_column_values(column='I')
        v_K = get_column_values(column='K')
        working_days = self.borelength_lfm/self.productivity
        tCO2eq = 0.0
        tCO2eq += 2*working_days*v_I*v_G/v_H * v_K
        return tCO2eq


    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        """
        self.out_material_production, tCO2eq_material_tranport = self.get_material_production()
        self.out_material_transport = self.get_material_transport(tCO2eq_material_tranport)
        self.out_disposal_transport = self.get_disposal_transport()
        self.out_equipment = self.get_equipment()
        self.out_energy_electricity_hour = self.get_energy_electricity_hour()
        self.out_mob_demob = self.get_mob_demob()
        self.out_persons_transport = self.get_persons_transport()

        return sum([self.out_material_production, self.out_material_transport, self.out_disposal_transport, self.out_equipment,
                    self.out_energy_electricity_hour, self.out_mob_demob, self.out_persons_transport])


if __name__ == '__main__':
    wall = PileWall()
    print(dir(wall))
    print(wall.borelength_lfm)
    print(issubclass(PileWall, BaseWall))
    print(isinstance(wall, BaseWall))
    print(PileWall.__mro__)