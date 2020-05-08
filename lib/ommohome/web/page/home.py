from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import log
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

#################################################
#                 Navigations                   #
#################################################
def logout(webdriver, waiting_time=30):
	try:
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
		print(traceback.format_exc())
		return False