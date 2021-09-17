import importlib

from db import DbModel


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


class Location(DbModel):

    @staticmethod
    def new_location(db, address, db_model='Mexico'):
        """

        :param db_model: which model to use for storing location data, must be used
        :param db: database
        :param address: address of the hotel
        :return: Location object
        """
        location_cls = class_for_name(f'locations.{db_model.lower()}', db_model)
        return location_cls(db, address)

    @staticmethod
    def load(db, location_id, db_model):
        location_cls = class_for_name(f'locations.{db_model.lower()}', db_model)
        return location_cls.load(db, location_id)
