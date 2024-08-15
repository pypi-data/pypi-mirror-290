# project_software_entwicklung_2\ensemble_package\__init__.py
# Author: Florian Meier

'''File for intializing the ensemble package'''


__all__ = ['ensemble_regressor_class', 'regressor_class', 'unit_testing']

# import the modules
from . import ensemble_regressor_class
from . import regressor_class
from . import unit_testing

# define the version

version = '1.0'