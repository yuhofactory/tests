from ConfigParser import SafeConfigParser
import os

def get_config():
	config = SafeConfigParser()
	config_filename = "config_resource.conf"
	config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_filename)

	if os.path.exists(config_filepath) == False:
		config_filepath = os.path.join(os.getenv("HOME"), ".tests_conf", config_filename)

	config.read(config_filepath)

	return config
