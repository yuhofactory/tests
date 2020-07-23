from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
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
expand_product_details_button_xpath = "//span[contains(text(), 'More (')]\
	//parent::button[contains(@class, 'shopee-button--link')]"
product_variation_items_xpath = "//div[@class='product-variation-item']"
sold_out_stock_labels_xpath = "//div[contains(@class, 'product-variation__stock')]\
	//descendant::div[text()='Sold out']|//descendant::span[text()='Sold out']"
zero_sales_labels_xpath = "//div[contains(@class, 'product-variation__sales') and text()='0']\
	|//div[contains(@class, 'product-variation__sales')]//descendant::div[text()='0']"
delisted_product_status_label_xpath = "//div[contains(@class, 'product-name')]/div[contains(text(), 'Delisted')]"
publish_button_xpath = "//span[contains(text(), 'Publish')]//parent::button"
delist_button_xpath = "//span[contains(text(), 'Delist')]//parent::button"

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
		input_filter_textfield = wait_event.until(ec.visibility_of_element_located(\
			(By.XPATH, input_filter_textfield_xpath)))
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
		scroll_to_product_details(webdriver)
		click_edit_button(webdriver, waiting_time)
		insert_stock_amount(webdriver, stock_amount_2Dlist, waiting_time)
		click_update_button(webdriver, waiting_time)
		wait_for_successful_update_notification(webdriver, waiting_time)
		myproducts_log.info("Successfully updated stock amount for product {}".\
			format(stock_amount_2Dlist[0][SHOPEE_PRODUCT_NAME_INDEX]))

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def scroll_to_product_details(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		product_amount_label = wait_event.until(ec.visibility_of_element_located(\
				(By.XPATH, product_amount_label_xpath)))
		# Scroll down as close as possible to the edit button to ensure its visibility
		product_amount_label.location_once_scrolled_into_view
		myproducts_log.debug("Successfully scrolled to product details")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def expand_product_details(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		expand_product_details_button = wait_event.until(ec.element_to_be_clickable(\
			(By.XPATH, expand_product_details_button_xpath)))
		expand_product_details_button.click()
		myproducts_log.debug("Successfully expanded product details")

	except Exception as e:
		myproducts_log.warning("No need to expand product details")

def get_product_variation_items_amount(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		product_variation_items_amount = None
		product_variation_items = wait_event.until(ec.visibility_of_all_elements_located(\
			(By.XPATH, product_variation_items_xpath)))
		product_variation_items_amount = len(product_variation_items)
		myproducts_log.debug("Successfully retrieved product variation items amount")

	except Exception as e:
		product_variation_items_amount = 1
		myproducts_log.warning("Selected product does not have variation")
		myproducts_log.warning(traceback.print_exc())

	return product_variation_items_amount

def get_sold_out_stock_amount(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		sold_out_stock_amount = None
		sold_out_stock_labels = wait_event.until(ec.visibility_of_all_elements_located(\
			(By.XPATH, sold_out_stock_labels_xpath)))
		sold_out_stock_amount = len(sold_out_stock_amount_labels)
		myproducts_log.debug("Successfully retrieved sold out stock amount")

	except Exception as e:
		sold_out_stock_amount = 0
		myproducts_log.warning("Product variations have not sold out yet")
		myproducts_log.warning(traceback.print_exc())

	return sold_out_stock_amount

def get_zero_sales_amount(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		zero_sales_amount = None
		zero_sales_labels = wait_event.until(ec.visibility_of_all_elements_located(\
			(By.XPATH, zero_sales_labels_xpath)))
		zero_sales_amount = len(zero_sales_amount_labels)
		myproducts_log.debug("Successfully retrieved zero sales amount")

	except Exception as e:
		zero_sales_amount = 0
		myproducts_log.warning("Product variations have sales records")
		myproducts_log.warning(traceback.print_exc())

	return zero_sales_amount

def get_delisted_product_status(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		delisted_product_status = True
		delisted_product_status_label = wait_event.until(ec.visibility_of_element_located(\
			(By.XPATH, delisted_product_status_label_xpath)))
		myproducts_log.debug("Successfully retrieved delisted product status")

	except Exception as e:
		delisted_product_status = False
		myproducts_log.warning("The product is not being delisted")

	return delisted_product_status

def click_publish_button(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		publish_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, publish_button_xpath)))
		publish_button.click()
		myproducts_log.debug("Successfully clicked publish button in product details page")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def click_delist_button(webdriver, waiting_time=30):
	try:
		wait_event = WebDriverWait(webdriver, waiting_time)
		delist_button = wait_event.until(ec.element_to_be_clickable((By.XPATH, delist_button_xpath)))
		delist_button.click()
		myproducts_log.debug("Successfully clicked delist button in product details page")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

def publish_delist_product(webdriver, waiting_time=30):
	try:
		scroll_to_product_details(webdriver, waiting_time=10)
		expand_product_details(webdriver, waiting_time=5)
		product_variation_items_amount = get_product_variation_items_amount(webdriver, waiting_time)
		sold_out_stock_amount = get_sold_out_stock_amount(webdriver, waiting_time)
		zero_sales_amount = get_zero_sales_amount(webdriver, waiting_time)
		delisted_product_status = get_delisted_product_status(webdriver, waiting_time)
		publish_delist_product_status = get_publish_delist_product_status(product_variation_items_amount, \
			sold_out_stock_amount, zero_sales_amount, delisted_product_status)

		if publish_delist_product_status is not None:
			click_edit_button(webdriver)

			if publish_delist_product_status == "publish":
				click_publish_button(webdriver)

			elif publish_delist_product_status == "delist":
				click_delist_button(webdriver)

			wait_for_successful_update_notification(webdriver)
			myproducts_log.info("Successfully {}ed the selected product".format(publish_delist_product_status))

		else:
			myproducts_log.info("No publish/delist process is required for the selected product")

	except Exception as e:
		myproducts_log.error(traceback.print_exc())

#################################################
#                  Operations                   #
#################################################
def get_publish_delist_product_status(product_variation_items_amount, sold_out_stock_amount, \
	zero_sales_amount, delisted_product_status):
	publish_delist_product_status = None

	# Delist product if all variations of the product are sold out and have no sales records
	if sold_out_stock_amount == product_variation_items_amount and \
		zero_sales_amount == product_variation_items_amount:

		# Delist product if it's currently being published
		if delisted_product_status == False:
			publish_delist_product_status = "delist"
		else:
			publish_delist_product_status = None

	else:
		# Publish product if it's currently being delisted
		if delisted_product_status:
			publish_delist_product_status = "publish"
		else:
			publish_delist_product_status = None

	return publish_delist_product_status
