from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import log
import ommohome.config as config

page = {
	"name"         : "login",
	"title"        : "OMMO Home - Home & Lifestyle",
	"parent"       : None,
	"url"          : "/my-account-2",
	"active_xpath" : None,
	"link_xpath"   : None,
	"ident_xpath"  : "//div[@class='text-copyright' and contains(text(), 'All Rights Reserved')]",
	"ident_id"     : None,
}

conf = config.get_config()
login_log = log.get_logger(logger_name="lib.ommohome.web.page.login", logging_level=conf.get("LOGGING", "LEVEL"))
username_input_xpath = "//input[@class='input-text username' and ancestor::form[@class='login']]"
password_input_xpath = "//input[@class='input-text password' and ancestor::form[@class='login']]"
login_button_xpath = "//input[@id='mr-login']"
login_menu_xpath = "//span[@class='t-text' and contains(text(), 'Log in')]//ancestor::a[@id='menu-extra-login']"

#################################################
#                 Navigations                   #
#################################################
def click_login_menu(webdriver, wait_event):
	try:
		login_menu = wait_event.until(ec.element_to_be_clickable((By.XPATH, login_menu_xpath)))
		login_menu.click()
		login_log.debug("Successfully click login menu")
		return True

	except:
		login_log.error("Failed to click login menu")
		login_log.error(traceback.print_exc())
		return False

def enter_username(webdriver, wait_event, username):
	try:
		username_input = wait_event.until(ec.visibility_of_element_located((By.XPATH, username_input_xpath)))
		username_input.send_keys(username)
		login_log.debug("Successfully enter username")
		return True

	except:
		login_log.error("Failed to enter username")
		login_log.error(traceback.print_exc())
		return False

def enter_password(webdriver, wait_event, password):
	try:
		password_input = wait_event.until(ec.visibility_of_element_located((By.XPATH, password_input_xpath)))
		password_input.send_keys(password)
		login_log.debug("Successfully enter password")
		return True

	except:
		login_log.error("Failed to enter password")
		login_log.error(traceback.print_exc())
		return False

def click_login_button(webdriver, wait_event):
	try:
		login_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, login_button_xpath)))
		login_button.click()
		login_log.debug("Successfully click login button")
		return True

	except:
		login_log.error("Failed to click login button")
		login_log.error(traceback.print_exc())
		return False

def login(webdriver, username, password, waiting_time=30):
	webdriver.get("https://ommohome.my")
	wait_event = WebDriverWait(webdriver, waiting_time)
	status = []
	status.append(click_login_menu(webdriver, wait_event))
	status.append(enter_username(webdriver, wait_event, username))
	status.append(enter_password(webdriver, wait_event, password))
	status.append(click_login_button(webdriver, wait_event))

	if False in status:
		login_log.error("Failed to login")
		return False
	else:
		login_log.info("Successfully login")
		return True