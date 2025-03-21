import configparser
import os

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file from the resources folder
config.read(os.path.join('resources', 'config.cfg'))

# Access the values from the 'API' section
BASE_URL = config['API']['BASE_URL']
TIMEOUT = int(config['API']['TIMEOUT'])
TOKEN = config['API']['TOKEN']
