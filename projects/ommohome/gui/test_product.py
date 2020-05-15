from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pytest
import ommohome.web.page.login as login
import ommohome.web.page.home as home
import ommohome.web.page.product as product
import ommohome.config as config
import resource.stock as stock
import traceback
import log

class TestProduct:

	@pytest.fixture(autouse=True)
	def setup(self, request):
		conf = config.get_config()

		if conf.get("WEBDRIVER_OPTIONS", "HEADLESS") == "True":
			options = Options()
			options.headless = True
			self.webdriver = webdriver.Firefox(options=options)

		else:
			self.webdriver = webdriver.Firefox()

		login.login(self.webdriver, username=conf.get("LOGIN", "EMAIL"), \
			password=conf.get("LOGIN", "PASSWORD"))

		def teardown():
			home.logout(self.webdriver)
			self.webdriver.quit()

		request.addfinalizer(teardown)

	def test_stock_amount_retrieval(self):
		OMMOHOME_PRODUCT_NAME_INDEX = 0
		stock_amount_3Dlist = stock.get_stock_amount(product_index_name="ommohome_product_name")
		new_stock_amount_list = []

		for i in range(len(stock_amount_3Dlist)):
			home.search_product(self.webdriver, stock_amount_3Dlist[i][0][OMMOHOME_PRODUCT_NAME_INDEX])
			stock_amount_list = product.select_product_variation(self.webdriver, stock_amount_3Dlist[i])

			for j in range(len(stock_amount_list)):
				new_stock_amount_list.append(stock_amount_list[j])

		stock.set_stock_amount(new_stock_amount_list)
