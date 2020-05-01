from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import log
import traceback
import shopee.config as config
import shopee.web.page.home as home
import shopee.web.page.myproducts as myproducts

conf = config.get_config()
nav_log = log.get_logger(logger_name="lib.shopee.web.nav", logging_level=conf.get("LOGGING", "LEVEL"))

def find_element(wait_event, ident_method, ident_str):
	# Note: Calling function should handle exception
	if ident_method == "xpath":
		wait_event.until(ec.visibility_of_element_located((By.XPATH, ident_str)))
	elif ident_method == "id":
		wait_event.until(ec.visibility_of_element_located((By.ID, ident_str)))
	else:
		nav_log.error("Failed to find element with {} {}".format(ident_method, ident_str))
		raise Exception()

# Check for existence of page
def is_page(wait_event, page):
	try:
		#################################################
		#               Main tab - Home                 #
		#################################################
		if page == "home":
			find_element(wait_event, "xpath", home.page["link_xpath"])
			find_element(wait_event, "id", home.page["ident_xpath"])
		#################################################
		#           Main tab - My Products              #
		#################################################
		elif page == "myproducts":
			find_element(wait_event, "xpath", myproducts.page["link_xpath"])
			find_element(wait_event, "xpath", myproducts.page["ident_xpath"])

	except Exception as e:
		nav_log.error(e)

def navigate(webdriver, page, use_url=False, waiting_time=30):
	if page == "home":
		page_nav = home.page
	elif page == "myproducts":
		page_nav = myproducts.page
	else:
		nav_log.error("No {} page found".format(page))

	if use_url:
		url = "https://seller.shopee.com.my/" + page_nav["url"]
		webdriver.get(url)
		nav_log.info("Successfully navigated to {} URL".format(page_nav["name"]))
	else:
		try:
			wait_event = WebDriverWait(webdriver, waiting_time)
			element = wait_event.until(ec.element_to_be_clickable((By.XPATH, page_nav["link_xpath"])))
			element.click()
			nav_log.info("Successfully navigated to {} page".format(page_nav["name"]))
		except Exception as e:
			nav_log.error(traceback.print_exc())
