from abc import ABC, abstractmethod
from random import randint


class BaseWall_EPD(ABC):
    """ Base class for wall"""
    def __init__(self, project_name='Sample project', classification=int(1), unit_co2_A1_to_A3=33.1, unit_co2_A5=20.6):
        self.id = randint(10100, 99999)
        self.project_name = project_name                        # used for referencing to which project the structure belongs to
        self.classification = classification                    # class 1, cement weight from 60 kg/m^3 to 100 kg/m^3
        self.unit_co2_A1_to_A3 = unit_co2_A1_to_A3          # kg CO2_eq per m^3
        self.unit_co2_A5 = unit_co2_A5                          # kg CO2_eq per m^3
    

    @abstractmethod
    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        To be implemented in concrete class
        """
        pass

