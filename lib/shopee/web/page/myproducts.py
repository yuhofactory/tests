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
variation_information_label_xpath = "//div[@class='edit-label edit-title' and contains(text(), 'Variation Information')]"
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
sales_information_label_xpath = "//h2[contains(text(), 'Sales Information')]"
stock_amount_textfield_xpath = "//h2[contains(text(), 'Sales Information')]//following-sibling::div\
	//descendant::input[@class='shopee-input__input' and ancestor::div[@class='grid edit-row']\
	//descendant::span[contains(text(), 'Stock')]]"
update_button_xpath = "//span[contains(text(), 'Update')]//parent::button[contains(@class, 'shopee-button')]"
successful_product_update_notification_xpath = "//div[@class='shopee-toasts']"
product_amount_label_xpath = "//div[@class='page-title' and contains(text(), 'product')]"

SHOPEE_PRODUCT_NAME_INDEX = 0
SHOPEE_VARIATION_TYPE_INDEX = 1
SHOPEE_VARIATION_DATA_INDEX = 2
PREVIOUS_AMOUNT_INDEX = 3
CURRENT_AMOUNT_INDEX = 4

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
		product_amount_label = wait_event.until(ec.visibility_of_element_located(\
				(By.XPATH, product_amount_label_xpath)))
		# Scroll down as close as possible to the edit button to ensure its visibility
		product_amount_label.location_once_scrolled_into_view
		edit_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, edit_button_xpath)))
		edit_button.click()
		myproducts_log.debug("Successfully clicked edit button in product table")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def insert_stock_amount(webdriver, stock_amount_2Dlist, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)

		# Retrieve all required web elements (for product with variation)
		if stock_amount_2Dlist[0][SHOPEE_VARIATION_TYPE_INDEX].upper() != "N/A" and \
			stock_amount_2Dlist[0][SHOPEE_VARIATION_DATA_INDEX].upper() != "N/A":
			variation_information_label = wait_event.until(ec.visibility_of_element_located(\
					(By.XPATH, variation_information_label_xpath)))
			variation_information_label.location_once_scrolled_into_view

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

			myproducts_log.debug("No of column data input (editable & non-editable) : {}".format(\
				len(column_data_input)))
			myproducts_log.debug("No of variation column data : {}".format(len(variation_column_data)))
			myproducts_log.debug("No of variation column header : {}".format(len(variation_column_header)))

		# Update stock amount for all variations of the same product
		for stock_amount in stock_amount_2Dlist:
			# For product with variation
			if stock_amount[SHOPEE_VARIATION_TYPE_INDEX].upper() != "N/A" and stock_amount[SHOPEE_VARIATION_DATA_INDEX].upper() != "N/A":
				stock_row_index = 0
				node_index = 0
				
				# Check for correct variation combination based on condition of parent node attribute
				while node_index < len(variation_column_data):
					is_product_variation = False
					is_found_stock_row_index = False
					variation_column_data_parent_attribute = get_parent_node_attribute(variation_column_data, node_index)

					# Check for parent node attribute in the first variation column
					while "table-row" in variation_column_data_parent_attribute:
						if variation_column_data[node_index].text in stock_amount[SHOPEE_VARIATION_DATA_INDEX].split("|"):
							is_product_variation = True

						node_index += 1
						stock_row_index += 1

						if node_index < len(variation_column_data):
							variation_column_data_parent_attribute = get_parent_node_attribute(variation_column_data, node_index)

						# Check for existence of second variation column
						if "table-cells" in variation_column_data_parent_attribute:
							stock_row_index -= 1
							break

						# Determine the index of stock amount row for variation with one column
						elif is_product_variation:
							stock_row_index -= 1
							is_found_stock_row_index = True
							break

					# Check for parent node attribute in the second variation column (if any)
					while "table-cells" in variation_column_data_parent_attribute:
						# Determine the index of stock amount row for variation with two columns
						if is_product_variation and variation_column_data[node_index].text in stock_amount[SHOPEE_VARIATION_DATA_INDEX].split("|"):
							is_found_stock_row_index = True
							break

						node_index += 1
						stock_row_index += 1

						if node_index < len(variation_column_data):
							variation_column_data_parent_attribute = get_parent_node_attribute(variation_column_data, node_index)

					if is_found_stock_row_index:
						break

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

			# For product without variation
			else:
				sales_information_label = wait_event.until(ec.visibility_of_element_located(\
					(By.XPATH, sales_information_label_xpath)))
				sales_information_label.location_once_scrolled_into_view

				stock_amount_textfield = wait_event.until(ec.visibility_of_element_located(\
					(By.XPATH, stock_amount_textfield_xpath)))
				stock_amount_textfield.clear()
				stock_amount_textfield.send_keys(stock_amount[CURRENT_AMOUNT_INDEX])
				myproducts_log.debug("Successfully inserted new stock amount")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def get_parent_node_attribute(variation_column_data, node_index):
	variation_column_data_parent = variation_column_data[node_index].find_element_by_xpath("..")
	variation_column_data_parent_attribute = variation_column_data_parent.get_attribute("class")

	return variation_column_data_parent_attribute

def click_update_button(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		update_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, update_button_xpath)))
		update_button.click()
		myproducts_log.debug("Successfully clicked update button in product details page")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def wait_for_successful_update_notification(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		successful_product_update_notification = wait_event.until(ec.visibility_of_element_located(\
			(By.XPATH, successful_product_update_notification_xpath)))
		myproducts_log.debug("Successfully displayed product update notification")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def update_stock_amount(webdriver, stock_amount_2Dlist, waiting_time=30):
	try:
		time.sleep(3)
		click_edit_button(webdriver, waiting_time)
		insert_stock_amount(webdriver, stock_amount_2Dlist, waiting_time)
		click_update_button(webdriver, waiting_time)
		wait_for_successful_update_notification(webdriver, waiting_time)
		myproducts_log.info("Successfully updated stock amount for product {}".\
			format(stock_amount_2Dlist[0][SHOPEE_PRODUCT_NAME_INDEX]))

	except Exception as e:
		myproducts_log.error(traceback.print_exc())
