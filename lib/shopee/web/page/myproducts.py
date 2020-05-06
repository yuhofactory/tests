from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import time
import log
import shopee.config as config

page = {
	"name"         : "myproducts",
	"title"        : "Shopee Seller Centre",
	"parent"       : None,
	"url"          : "portal/product/list/all",
	"active_xpath" : None,
	"link_xpath"   : "//a[contains(@class, 'sidebar-submenu-item-link') and @href='/portal/product/list/all']",
	"ident_xpath"  : "//span[text()='Go']//ancestor::button[contains(@class, 'shopee-button')]",
	"ident_id"     : None,
}

conf = config.get_config()
myproducts_log = log.get_logger(logger_name="lib.shopee.web.page.myproducts", logging_level=conf.get("LOGGING", "LEVEL"))

invisible_element_xpath = "//div[@class='full-mask']"
new_list_view_popup_xpath = "//div[contains(@class, 'guide-modal')]"
element_removal_script = "arguments[0].parentNode.removeChild(arguments[0])"
element_invisibility_script = "arguments[0].style.visibility='hidden'"
input_filter_textfield_xpath = "//div[@class='filter-input']//descendant::input[@class='shopee-input__input' and @type='text']"
search_button_xpath = "//span[text()='Search']//ancestor::button[contains(@class, 'shopee-button')]"
edit_button_xpath = "//div[@class='product-action']//child::button"
variation_information_xpath = "//div[@class='edit-label edit-title' and contains(text(), 'Variation Information')]"
variation_table_column_names_xpath = "//div[contains(text(), 'Variation List')]\
    //following-sibling::div//descendant::div[@class='table-header']//descendant::div[@class='table-cell']"
column_data_input_xpath = "//div[contains(text(), 'Variation List')]//following-sibling::div\
	//descendant::div[@class='table-cell']//descendant::input[contains(@class, 'shopee-input')]\
	|descendant::div[@class='table-cell-discount']|//div[contains(text(), 'Variation List')]//following-sibling::div\
	//descendant::div[@class='table-cell']//descendant::textarea[contains(@class, 'shopee-input')]"
variation_column_data_xpath = "//div[contains(text(), 'Variation List')]\
    //following-sibling::div//descendant::div[@class='table-body']//descendant::div[@class='table-cell readonly']"
variation_column_header_xpath = "//div[contains(text(), 'Variation List')]\
    //following-sibling::div//descendant::div[@class='table-header']//descendant::div[@class='table-cell readonly']"

OMMOHOME_PRODUCT_INDEX = 0
SHOPEE_PRODUCT_INDEX = 1
VARIATION_TYPE_INDEX = 2
VARIATION_DATA_INDEX = 3
PREVIOUS_AMOUNT_INDEX = 4
CURRENT_AMOUNT_INDEX = 5

#################################################
#                 Navigations                   #
#################################################
def remove_new_list_view_popup(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		new_list_view_popup = wait_event.until(ec.presence_of_element_located(\
			(By.XPATH, new_list_view_popup_xpath)))
		
		webdriver.execute_script(element_removal_script, new_list_view_popup)
		myproducts_log.debug("Successfully removed new list view popup")

		invisible_element = webdriver.find_element_by_xpath(invisible_element_xpath)
		webdriver.execute_script(element_invisibility_script, invisible_element)
		myproducts_log.debug("Successfully hide visibility of obscuring web element")

		# Make sure that the whole webpage is properly loaded before proceeding to next process
		wait_event.until(ec.presence_of_element_located((By.XPATH, page["ident_xpath"])))

	except Exception as e:
		pass

def insert_product_filter_input(webdriver, input, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		input_filter_textfield = wait_event.until(ec.visibility_of_element_located((By.XPATH, input_filter_textfield_xpath)))
		input_filter_textfield.clear()
		input_filter_textfield.send_keys(input)
		myproducts_log.debug("Successfully inserted product filter input")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def click_search_button(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		search_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, search_button_xpath)))
		search_button.click()
		myproducts_log.debug("Successfully clicked search button")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def search_product(webdriver, input, type="Product Name", waiting_time=30):
	try:
		time.sleep(5)
		insert_product_filter_input(webdriver, input, waiting_time)
		click_search_button(webdriver, waiting_time)
		myproducts_log.info("Successfully filtered product {}".format(input))

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def click_edit_button(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		edit_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, edit_button_xpath)))
		edit_button.click()
		myproducts_log.debug("Successfully clicked edit button in product table")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def insert_stock_amount(webdriver, stock_amount, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)

		# For product with variation
		if stock_amount[VARIATION_TYPE_INDEX].upper() != "N/A" and stock_amount[VARIATION_DATA_INDEX].upper() != "N/A":
			variation_information = wait_event.until(ec.visibility_of_element_located(\
				(By.XPATH, variation_information_xpath)))
			variation_information.location_once_scrolled_into_view

			variation_table_column_names = wait_event.until(ec.visibility_of_all_elements_located(\
				(By.XPATH, variation_table_column_names_xpath)))
			myproducts_log.debug("Successfully retrieved variation table column names")

			STOCK_COLUMN_INDEX = 0

			for i in range(len(variation_table_column_names)):
				if str(variation_table_column_names[i].text).strip().upper() != "STOCK":
					STOCK_COLUMN_INDEX += 1
				else:
					myproducts_log.debug("STOCK_COLUMN_INDEX : {}".format(STOCK_COLUMN_INDEX))
					break

			column_data_input = wait_event.until(ec.visibility_of_all_elements_located(\
				(By.XPATH, column_data_input_xpath)))
			variation_column_data = wait_event.until(ec.visibility_of_all_elements_located(\
				(By.XPATH, variation_column_data_xpath)))
			variation_column_header = wait_event.until(ec.visibility_of_all_elements_located(\
				(By.XPATH, variation_column_header_xpath)))

			no_of_variation = len(variation_column_header)
			stock_row_index = 0

			myproducts_log.debug("No of column data input (editable & non-editable) : {}".format(\
				len(column_data_input)))
			myproducts_log.debug("No of variation column data : {}".format(len(variation_column_data)))
			myproducts_log.debug("No of variation column header : {}".format(len(variation_column_header)))

			# Check for correct variation combination in the table based on input file
			for i in range(0, len(variation_column_data), no_of_variation):
				is_product_variation = True

				for j in range(i, i+no_of_variation, 1):
					myproducts_log.debug("Searching for non-existence of {} in {} : {}".format(\
						variation_column_data[j].text, \
						stock_amount[VARIATION_DATA_INDEX].split("|"), \
						variation_column_data[j].text not in stock_amount[VARIATION_DATA_INDEX].split("|")))

					if variation_column_data[j].text not in stock_amount[VARIATION_DATA_INDEX].split("|"):
						is_product_variation = False
						break

				if is_product_variation:
					break
				else:
					stock_row_index += 1
			
			myproducts_log.debug("Correct variation combination is at row index {}".format(stock_row_index))
			row = 0

			# Update stock amount based on its variation combination
			for i in range(STOCK_COLUMN_INDEX, len(column_data_input), len(variation_table_column_names)):
				if row == stock_row_index:
					column_data_input[i].clear()
					column_data_input[i].send_keys(stock_amount[CURRENT_AMOUNT_INDEX])
					myproducts_log.debug("Successfully inserted new stock amount")
					break
				else:
					row += 1

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def update_stock_amount(webdriver, stock_amount, waiting_time=30):
	try:
		time.sleep(3)
		click_edit_button(webdriver, waiting_time)
		insert_stock_amount(webdriver, stock_amount, waiting_time)
		myproducts_log.info("Successfully updated stock amount for product {} from {} unit to {} unit".\
			format(stock_amount[SHOPEE_PRODUCT_INDEX], stock_amount[PREVIOUS_AMOUNT_INDEX], \
				stock_amount[CURRENT_AMOUNT_INDEX]))

	except Exception as e:
		myproducts_log.error(traceback.print_exc())
