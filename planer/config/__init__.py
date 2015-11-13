
from xdg import BaseDirectory
import configparser
import os
import sys
from pprint import pprint

# Configuring the config filename
_appname = (__package__ or 'planer.daemon').split('.')[0]
_config_file = _appname + '.conf'
_defaults_file = os.path.join(__path__[0], _config_file)


# Read default and user configurations
config = configparser.ConfigParser()
with open(_defaults_file) as f: config.read_file(f, "defaults")
config.read(os.path.join(path, _config_file)
            for path in BaseDirectory.load_config_paths(_appname))


# Database is absolute or relative to the xdg data home.
_database_file = config['daemon']['database file']
_database_file = os.path.expanduser(_database_file)
if not os.path.isabs(_database_file):
    config['daemon']['database file'] = os.path.join(
            BaseDirectory.save_data_path(_appname),
            config['daemon']['database file'])


