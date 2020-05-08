from ConfigParser import SafeConfigParser
import os

def get_config():
	config = SafeConfigParser()
	home_dir = os.getenv("HOME")
	config.read("{}/.tests_conf/config_shopee.conf".format(home_dir))
	return config