import os
import configparser

config = configparser.ConfigParser()

# Ensure that the path to the config file is correct
config.read(os.path.join('resources', 'config.cfg'))

BASE_URL = config['API']['BASE_URL']
TIMEOUT = config.getint('API', 'TIMEOUT')
