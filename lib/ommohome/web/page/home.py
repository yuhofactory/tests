from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import traceback
import log
import time
import ommohome.config as config

page = {
	"name"         : "home",
	"title"        : "OMMO Home - Home & Lifestyle",
	"parent"       : None,
	"url"          : None,
	"active_xpath" : None,
	"link_xpath"   : "//a[@href='https://ommohome.my' and contains(text(), 'Home') and ancestor::div[@class='primary-nav nav']]",
	"ident_xpath"  : "//div[@class='text-copyright' and contains(text(), 'All Rights Reserved')]",
	"ident_id"     : None,
}

conf = config.get_config()
home_log = log.get_logger(logger_name="lib.ommohome.web.page.home", logging_level=conf.get("LOGGING", "LEVEL"))
username_menu_xpath = "//span[contains(text(), '{}')]//ancestor::li[contains(@class, 'logined')]".format(\
	conf.get("LOGIN", "EMAIL_USERNAME"))
logout_button_xpath = "//a[contains(text(), 'Logout') and ancestor::li[contains(@class, 'logined')]]"
account_label_xpath = "//h1[contains(text(), 'My Account')]"
search_textfield_xpath = "//input[@id='search-field-auto']"
search_dropdown_xpath = "//span[@class='product-title' and contains(text(), '{}')]//parent::a"

#################################################
#                 Navigations                   #
#################################################
def logout(webdriver, waiting_time=30):
	try:
		# Scroll to the top of page to ensure visibility of username menu
		webdriver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)
		wait_event = WebDriverWait(webdriver, waiting_time)
		action = ActionChains(webdriver)
		username_menu = wait_event.until(ec.visibility_of_element_located((By.XPATH, username_menu_xpath)))
		action.move_to_element(username_menu).perform()
		home_log.debug("Successfully hovered to user account menu")

		logout_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, logout_button_xpath)))
		logout_button.click()
		home_log.debug("Successfully clicked logout button")
		wait_event.until(ec.visibility_of_element_located((By.XPATH, account_label_xpath)))
		home_log.info("Successfully logout")
		return True

	except:
		home_log.error("Failed to logout")
		home_log.error(traceback.print_exc())
		return False

def insert_product_name(webdriver, product_name, waiting_time=30):
	try:
		# Scroll to the top of page to ensure visibility of search textfield
		webdriver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)
		wait_event = WebDriverWait(webdriver, waiting_time)
		search_textfield = wait_event.until(ec.visibility_of_element_located((By.XPATH, search_textfield_xpath)))
		search_textfield.clear()
		search_textfield.send_keys(product_name)
		home_log.debug("Successfully inserted product name")

	except Exception as e:
		home_log.error(traceback.print_exc())

def click_product_name(webdriver, product_name, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		search_dropdown = wait_event.until(ec.element_to_be_clickable((By.XPATH, search_dropdown_xpath.format(\
			product_name))))
		search_dropdown.click()
		home_log.debug("Successfully clicked product name")

	except Exception as e:
		home_log.error(traceback.print_exc())

def search_product(webdriver, product_name, waiting_time=30):
	try:
		insert_product_name(webdriver, product_name, waiting_time)
		click_product_name(webdriver, product_name, waiting_time)
		home_log.info("Successfully searched product {}".format(product_name))

	except Exception as e:
		home_log.error(traceback.print_exc())
