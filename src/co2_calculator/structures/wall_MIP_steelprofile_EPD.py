import pandas as pd
import math
from src.co2_calculator.structures.wall_base_EPD import BaseWall_EPD

# for debugging
# from wall_base import wall_base

filename_database = './src/co2_calculator/documents/CO2-eq Fußabdruck - Vergleich Allgemein_bara.xlsx'

class MIPSteelProfileWall_EPD(BaseWall_EPD):
    """ Concrete class for pile walls"""
    def __init__(self, wall_area=3430.0, wall_thickness=0.55, classification='Class I', weight_steelprofile=270.0,
                unit_co2_A1_to_A3={'Class I': 37.3, 'Class II': 37.3, 'Class III': 37.3, 'Class IV': 37.3, 'Class V': 37.3, 'Class VI': 37.3}, 
                unit_co2_A5={'Class I': 20.6, 'Class II': 20.6, 'Class III': 20.6, 'Class IV': 20.6, 'Class V': 20.6, 'Class VI': 20.6}):
        super().__init__()
        self.classification = classification                # class 1, cement weight from 60 kg/m^3 to 100 kg/m^3
        self.unit_co2_A1_to_A3 = unit_co2_A1_to_A3          # kg CO2_eq per m^3
        self.unit_co2_A5 = unit_co2_A5                      # kg CO2_eq per m^3
        self.wall_area = wall_area                          # m^2
        self.wall_thickness = wall_thickness                # m
        self.weight_steelprofile = weight_steelprofile      # ton

        # dataframe (read from excel)
        self.df = self.read_database(columns='C,F,G,H,I,J,K,M,O', names=['C', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'O'])

        # outputs
        #self.

    def read_database(self, columns='C', names=['C']):
        """ Reads parameter stored in Excel database
        Note: time consuming!!
        """
        df = pd.read_excel(filename_database, sheet_name='Calculations MIP-VW', usecols=columns, names=names)
        df = df.fillna(0.0)
        return df


    def get_material_production_steel(self):
        """ Gets tCO2_eq by the production of steel only
        """
        df = self.df['K']
        vK_steel =       float(df.iloc[19])
        tCO2eq = 0.0
        tCO2eq += vK_steel*self.weight_steelprofile
        return tCO2eq


    def get_material_transport_steel(self):
        """ Gets tCO2_eq by the transport of steel only
        """
        def get_column_values(column='K'):
            """ gets values from table, column K"""
            df = self.df[column]
            v_steel =           float(df.iloc[52])
            return v_steel

        def get_transport_times(G,I):
            """ gets transport times, column M"""
            return math.ceil(G/I)

        vI_steel = get_column_values(column='I')
        vJ_steel = get_column_values(column='J')
        vK_steel = get_column_values(column='K')
        vO_steel = get_column_values(column='O')
        tCO2eq = 0.0
        tCO2eq += vJ_steel*get_transport_times(self.weight_steelprofile, vI_steel)*vK_steel*(1.0+vO_steel/100)
        return tCO2eq

    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        """
        tco2_eq = 0.0
        tco2_eq += self.get_material_production_steel()
        tco2_eq += self.get_material_transport_steel()
        tco2_eq += self.wall_area*self.wall_thickness*(self.unit_co2_A1_to_A3[self.classification] + self.unit_co2_A5[self.classification])*0.001     # ton

        return tco2_eq
