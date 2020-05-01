from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import log
import shopee.config as config

page = {
	"name"         : "myproducts",
	"title"        : "Shopee Seller Centre",
	"parent"       : None,
	"url"          : "portal/product/list/all",
	"active_xpath" : None,
	"link_xpath"   : "//a[contains(@class, 'sidebar-submenu-item-link') and @href='/portal/product/list/all']",
	"ident_xpath"  : "//button[contains(@class, 'shopee-button')]//descendant::span[text()='Go']",
	"ident_id"     : None,
}

conf = config.get_config()
myproducts_log = log.get_logger(logger_name="lib.shopee.web.page.myproducts", logging_level=conf.get("LOGGING", "LEVEL"))
invisible_element_xpath = "//div[@class='full-mask']"
new_list_view_popup_xpath = "//div[contains(@class, 'guide-modal')]"
element_removal_script = "arguments[0].parentNode.removeChild(arguments[0])"
element_invisibility_script = "arguments[0].style.visibility='hidden'"

#################################################
#                 Navigations                   #
#################################################
def remove_new_list_view_popup(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		new_list_view_popup = wait_event.until(ec.presence_of_element_located((By.XPATH, new_list_view_popup_xpath)))
		
		webdriver.execute_script(element_removal_script, new_list_view_popup)
		myproducts_log.debug("Successfully removed new list view popup")

		invisible_element = webdriver.find_element_by_xpath(invisible_element_xpath)
		webdriver.execute_script(element_invisibility_script, invisible_element)
		myproducts_log.debug("Successfully hide visibility of obscuring web element")

	except Exception as e:
		myproducts_log.error(e)