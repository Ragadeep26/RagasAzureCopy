import pandas as pd
import math
from src.co2_calculator.structures.wall_base_EPD import BaseWall_EPD

# for debugging
# from wall_base import wall_base

filename_database = './src/co2_calculator/documents/CO2-eq Fußabdruck - Vergleich Allgemein_bara.xlsx'

class MIPWall_EPD(BaseWall_EPD):
    """ Concrete class for pile walls"""
    def __init__(self, wall_area=3430.0, wall_thickness=0.55, classification='Class I', 
                unit_co2_A1_to_A3={'Class I': 37.3, 'Class II': 37.3, 'Class III': 37.3, 'Class IV': 37.3, 'Class V': 37.3, 'Class VI': 37.3}, 
                unit_co2_A5={'Class I': 20.6, 'Class II': 20.6, 'Class III': 20.6, 'Class IV': 20.6, 'Class V': 20.6, 'Class VI': 20.6}):
        super().__init__()
        self.classification = classification                # class 1, cement weight from 60 kg/m^3 to 100 kg/m^3
        self.unit_co2_A1_to_A3 = unit_co2_A1_to_A3          # kg CO2_eq per m^3
        self.unit_co2_A5 = unit_co2_A5                      # kg CO2_eq per m^3
        self.wall_area = wall_area                          # m^2
        self.wall_thickness = wall_thickness                # m

        # outputs
        #self.


    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        """
        tco2_eq = self.wall_area*self.wall_thickness*(self.unit_co2_A1_to_A3[self.classification] + self.unit_co2_A5[self.classification])*0.001     # ton

        return tco2_eq
