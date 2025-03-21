import configparser
import os

# Initialize configparser
config = configparser.ConfigParser()

# Construct the correct path to the config.cfg file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

# Log the config file path to verify if it is correct
print(f"Config file path: {config_file_path}")

# Read the configuration file and check if it's being read correctly
if os.path.exists(config_file_path):
    print("Config file found!")
    config.read(config_file_path)
else:
    print("Config file not found!")

# Access values from the [API] section
try:
    BASE_URL = config['API']['BASE_URL']
    TIMEOUT = int(config['API']['TIMEOUT'])
    print(f"Base URL: {BASE_URL}, Timeout: {TIMEOUT}")
except KeyError as e:
    print(f"KeyError: {e}")
