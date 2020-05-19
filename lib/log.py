import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
import resource.config as config

FORMATTER = logging.Formatter("%(asctime)s [%(name)s][%(levelname)s] %(message)s")
conf = config.get_config()
LOG_FILE = os.path.join(conf.get("LOGGING", "LOGFILEPATH"), "tests.log")

def get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

def get_file_handler():
	file_handler = TimedRotatingFileHandler(filename=LOG_FILE, when="midnight")
	file_handler.setFormatter(FORMATTER)
	return file_handler

def get_logger(logger_name, logging_level):
	logger = logging.getLogger(logger_name)

	if logging_level == "debug":
		logger.setLevel(logging.DEBUG)
	elif logging_level == "info":
		logger.setLevel(logging.INFO)
	elif logging_level == "warning":
		logger.setLevel(logging.WARNING)
	elif logging_level == "error":
		logger.setLevel(logging.ERROR)
	elif logging_level == "critical":
		logger.setLevel(logging.CRITICAL)

	logger.addHandler(get_console_handler())
	logger.addHandler(get_file_handler())
	return logger
