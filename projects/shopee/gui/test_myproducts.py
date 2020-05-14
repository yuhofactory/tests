from selenium import webdriver
import pytest
import shopee.web.page.login as login
import shopee.web.page.home as home
import shopee.web.page.myproducts as myproducts
import shopee.web.nav as nav
import shopee.config as config
import resource.stock as stock
import traceback
import log
import time

class TestMyProducts:

	@pytest.fixture(autouse=True)
	def setup(self, request):
		self.webdriver = webdriver.Firefox()
		conf = config.get_config()
		login.login(self.webdriver, username=conf.get("LOGIN", "USERNAME"), \
			password=conf.get("LOGIN", "PASSWORD"))

		def teardown():
			home.logout(self.webdriver)
			self.webdriver.quit()

		request.addfinalizer(teardown)

	def test_stock_amount_update(self):
		SHOPEE_PRODUCT_NAME_INDEX = 0

		stock_amount_3Dlist = stock.get_stock_amount(product_index_name="shopee_product_name")
		nav.navigate(self.webdriver, "myproducts", use_url=True)
		myproducts.remove_new_list_view_popup(self.webdriver)

		for i in range(len(stock_amount_3Dlist)):
			if len(stock_amount_3Dlist[i]) > 0:
				myproducts.search_product(self.webdriver, input=stock_amount_3Dlist[i][0][SHOPEE_PRODUCT_NAME_INDEX])
				myproducts.update_stock_amount(self.webdriver, stock_amount_3Dlist[i])
				