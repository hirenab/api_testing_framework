import configparser
import os

# Initialize configparser
config = configparser.ConfigParser()

# Path to the config.cfg file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

# Read the configuration file
config.read(config_file_path)

# Access values from the [API] section
BASE_URL = config['API']['BASE_URL']
TIMEOUT = int(config['API']['TIMEOUT'])
