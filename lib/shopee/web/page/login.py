from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback

page = {
	"name"         : "login",
	"title"        : "Login",
	"parent"       : None,
	"path"         : "login",
	"active_xpath" : None,
	"link_xpath"   : None,
	"ident_xpath"  : "//div[@class='signin-title' and contains(text(), 'Shopee Seller Centre')]",
	"ident_id"     : None,
}

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
		return True

	except:
		print(traceback.format_exc())
		return False

def enter_password(webdriver, wait_event, password):
	try:
		password_input = wait_event.until(ec.visibility_of_element_located((By.XPATH, password_input_xpath)))
		password_input.send_keys(password)
		return True

	except:
		print(traceback.format_exc())
		return False

def click_login_button(webdriver, wait_event):
	try:
		login_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, login_button_xpath)))
		login_button.click()
		return True

	except:
		print(traceback.format_exc())
		return False

def login(webdriver, username, password, waiting_time=30):
	webdriver.get("https://seller.shopee.com.my")
	wait_event = WebDriverWait(webdriver, waiting_time)
	enter_username(webdriver, wait_event, username)
	enter_password(webdriver, wait_event, password)
	click_login_button(webdriver, wait_event)