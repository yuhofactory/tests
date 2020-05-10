from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import time
import log
import ommohome.config as config

page = {
	"name"         : "product",
	# The page title contains the product name, ex: Utensil Canister - OMMO Home
	"title"        : "{} - OMMO Home",
	"parent"       : None,
	"url"          : None,
	"active_xpath" : None,
	"link_xpath"   : None,
	"ident_xpath"  : "//h2[contains(text(), 'Related products')]",
	"ident_id"     : None,
}

conf = config.get_config()
myproducts_log = log.get_logger(logger_name="lib.ommohome.web.page.product", logging_level=conf.get("LOGGING", "LEVEL"))

variation_dropdown_xpath = "//table[@class='variations']//descendant::td[child::label[@for='{}']]\
	//following-sibling::td//descendant::select[@id='{}']"
variation_dropdown_item_xpath = "{}/option[@value='{}']"
standard_policy_label_xpath = "//div[@class='entry-summary-content']//descendant::div[@class='woo-short-description']\
	//descendant::p[last()]"

OMMOHOME_PRODUCT_NAME_INDEX = 0
OMMOHOME_VARIATION_TYPE_INDEX = 1
OMMOHOME_VARIATION_DATA_INDEX = 2
PREVIOUS_AMOUNT_INDEX = 3
CURRENT_AMOUNT_INDEX = 4

#################################################
#                 Navigations                   #
#################################################
def select_product_variation(webdriver, product_variation_list_2Dlist, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		standard_policy_label = wait_event.until(ec.visibility_of_element_located(\
			(By.XPATH, standard_policy_label_xpath)))
		# Scroll down as close as possible to the product variation dropdown to ensure its visibility
		standard_policy_label.location_once_scrolled_into_view
		time.sleep(1)

		for product_variation_list in product_variation_list_2Dlist:
			# For product with variation only
			if product_variation_list[OMMOHOME_VARIATION_TYPE_INDEX] != "N/A" and product_variation_list[OMMOHOME_VARIATION_DATA_INDEX] != "N/A":
				variation_type_list = product_variation_list[OMMOHOME_VARIATION_TYPE_INDEX].split("|")
				variation_data_list = product_variation_list[OMMOHOME_VARIATION_DATA_INDEX].split("|")

				for i in range(len(variation_type_list)):
					variation_dropdown = wait_event.until(ec.element_to_be_clickable(\
						(By.XPATH, variation_dropdown_xpath.format(variation_type_list[i].lower(), \
							variation_type_list[i].lower()))))
					variation_dropdown.click()
					time.sleep(1)

					variation_dropdown_item = wait_event.until(ec.element_to_be_clickable(\
						(By.XPATH, variation_dropdown_item_xpath.format(variation_dropdown_xpath.format(\
							variation_type_list[i].lower(), variation_type_list[i].lower()), \
							variation_data_list[i]))))
					variation_dropdown_item.click()
					time.sleep(1)

					myproducts_log.debug("Successfully selected variation {} {} for product {}".format(\
						variation_type_list[i], variation_data_list[i], \
						product_variation_list[OMMOHOME_PRODUCT_NAME_INDEX]))

	except Exception as e:
		myproducts_log.error(traceback.print_exc())
