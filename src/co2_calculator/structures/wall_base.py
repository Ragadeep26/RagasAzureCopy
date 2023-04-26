from abc import ABC, abstractmethod
from random import randint


class BaseWall(ABC):
    """ Base class for wall"""
    def __init__(self, project_name='Sample project', productivity=200.0,
                 diesel=650.0, electricity=50.0, distance_mob_demob=250.0):
        self.id = randint(10100, 99999)
        self.project_name = project_name                            # used for referencing to which project the structure belongs to
        self.productivity = productivity                            # m/AT (Meter pro Arbeitstag)
        self.diesel = diesel                                        # liter/AT
        self.electricity = electricity                              # kWh/h
        self.distance_mob_demob = distance_mob_demob                # km
    

    @abstractmethod
    def read_database(self):
        """ Reads parameter stored in Excel database
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_material_production(self):
        """ Gets tCO2_eq by the production of material
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_material_transport(self):
        """ Gets tCO2_eq by the transport of material
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_disposal_transport(self):
        """ Gets tCO2_eq by disposal transport
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_equipment(self):
        """ Gets tCO2_eq by equipment
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_energy_electricity_hour(self):
        """ Gets tCO2_eq by energy electricity hour
        To be implemented in concrete class
        """
        pass


    @abstractmethod
    def get_mob_demob(self):
        """ Gets tCO2_eq by mobilization and demobilization
        """
        pass


    @abstractmethod
    def get_persons_transport(self):
        """ Gets tCO2_eq by transport of persons
        """
        pass
    

    @abstractmethod
    def calc_co2eq(self):
        """ Calculates equivalent CO2 emission tCO2eq
        To be implemented in concrete class
        """
        pass

