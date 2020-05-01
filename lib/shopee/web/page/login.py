from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import log
import shopee.config as config

page = {
	"name"         : "login",
	"title"        : "Shopee Seller Centre",
	"parent"       : None,
	"url"          : "account/signin",
	"active_xpath" : None,
	"link_xpath"   : None,
	"ident_xpath"  : "//div[@class='signin-title' and contains(text(), 'Shopee Seller Centre')]",
	"ident_id"     : None,
}

conf = config.get_config()
login_log = log.get_logger(logger_name="lib.shopee.web.page.login", logging_level=conf.get("LOGGING", "LEVEL"))
username_input_xpath = "//input[@class='shopee-input__input' and @placeholder='Email/Phone/Username']"
password_input_xpath = "//input[@class='shopee-input__input' and @placeholder='Password']"
login_button_xpath = "//button[descendant::span[text()='Log In']]"

#################################################
#                 Navigations                   #
#################################################
def enter_username(webdriver, wait_event, username):
	try:
		username_input = wait_event.until(ec.visibility_of_element_located((By.XPATH, username_input_xpath)))
		username_input.send_keys(username)
		login_log.debug("Successfully enter username")
		return True

	except:
		login_log.error("Failed to enter username")
		print(traceback.format_exc())
		return False

def enter_password(webdriver, wait_event, password):
	try:
		password_input = wait_event.until(ec.visibility_of_element_located((By.XPATH, password_input_xpath)))
		password_input.send_keys(password)
		login_log.debug("Successfully enter password")
		return True

	except:
		login_log.error("Failed to enter password")
		print(traceback.format_exc())
		return False

def click_login_button(webdriver, wait_event):
	try:
		login_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, login_button_xpath)))
		login_button.click()
		login_log.debug("Successfully click login button")
		return True

	except:
		login_log.error("Failed to click login button")
		print(traceback.format_exc())
		return False

def login(webdriver, username, password, waiting_time=30):
	webdriver.get("https://seller.shopee.com.my")
	wait_event = WebDriverWait(webdriver, waiting_time)
	status = []
	status.append(enter_username(webdriver, wait_event, username))
	status.append(enter_password(webdriver, wait_event, password))
	status.append(click_login_button(webdriver, wait_event))

	if False in status:
		login_log.error("Failed to login")
		return False
	else:
		login_log.info("Successfully login")
		return True