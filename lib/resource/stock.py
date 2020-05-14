import traceback
import log
import os
import pandas
import shutil
import shopee.config as config

conf = config.get_config()
stock_log = log.get_logger(logger_name="lib.resource.stock", logging_level=conf.get("LOGGING", "LEVEL"))
stock_amount_repo_path = "{}/input_file/stock_amount.csv".format(os.path.dirname(os.path.realpath(__file__)))
stock_amount_temp_path = "{}/Desktop/stock_amount.csv".format(os.getenv("HOME"))

def get_stock_amount(product_index_name):
	if os.path.exists(stock_amount_temp_path) == False:
		shutil.copy2(stock_amount_repo_path, stock_amount_temp_path)

	try:
		df_header = pandas.read_csv(stock_amount_temp_path, nrows=1)
		df_header_list = list(df_header.columns)
		df_stock_amount = pandas.read_csv(stock_amount_temp_path, \
			names=df_header_list, usecols=df_header_list, skiprows=1, keep_default_na=False)
		stock_amount_2Dlist = []
		stock_amount_3Dlist = []
		product_name = str(df_stock_amount.loc[0, product_index_name])

		for i in df_stock_amount.index:
			ommohome_product_name = str(df_stock_amount.loc[i, "ommohome_product_name"])
			ommohome_variation_type = str(df_stock_amount.loc[i, "ommohome_variation_type"])
			ommohome_variation_data = str(df_stock_amount.loc[i, "ommohome_variation_data"])
			shopee_product_name = str(df_stock_amount.loc[i, "shopee_product_name"])
			shopee_variation_type = str(df_stock_amount.loc[i, "shopee_variation_type"])
			shopee_variation_data = str(df_stock_amount.loc[i, "shopee_variation_data"])
			previous_amount = str(df_stock_amount.loc[i, "previous_amount"])
			current_amount = str(df_stock_amount.loc[i, "current_amount"])

			if product_index_name == "shopee_product_name":
				if product_name == shopee_product_name:
					stock_amount_2Dlist.append([
						shopee_product_name, 
						shopee_variation_type, 
						shopee_variation_data, 
						previous_amount,
						current_amount
					])
				else:
					stock_amount_3Dlist.append(stock_amount_2Dlist)
					stock_amount_2Dlist = []
					stock_amount_2Dlist.append([
						shopee_product_name, 
						shopee_variation_type, 
						shopee_variation_data, 
						previous_amount,
						current_amount
					])
					product_name = shopee_product_name

			elif product_index_name == "ommohome_product_name":
				if product_name == ommohome_product_name:
					stock_amount_2Dlist.append([
						ommohome_product_name, 
						ommohome_variation_type, 
						ommohome_variation_data, 
						previous_amount,
						current_amount
					])
				else:
					stock_amount_3Dlist.append(stock_amount_2Dlist)
					stock_amount_2Dlist = []
					stock_amount_2Dlist.append([
						ommohome_product_name, 
						ommohome_variation_type, 
						ommohome_variation_data, 
						previous_amount,
						current_amount
					])
					product_name = ommohome_product_name

		# Append the last 2D list
		stock_amount_3Dlist.append(stock_amount_2Dlist)
		stock_log.info("Successfully retrieved stock amount")

	except:
		stock_log.error(traceback.print_exc())

	return stock_amount_3Dlist

def set_stock_amount(stock_amount_list):
	if os.path.exists(stock_amount_temp_path) == False:
		shutil.copy2(stock_amount_repo_path, stock_amount_temp_path)

	try:
		df_header = pandas.read_csv(stock_amount_temp_path, nrows=1)
		df_header_list = list(df_header.columns)
		df_stock_amount = pandas.read_csv(stock_amount_temp_path, \
			names=df_header_list, usecols=df_header_list, skiprows=1, keep_default_na=False)

		for i in df_stock_amount.index:
			df_stock_amount.loc[i, "previous_amount"] = str(df_stock_amount.loc[i, "current_amount"])
			df_stock_amount.loc[i, "current_amount"] = stock_amount_list[i]

		df_stock_amount.to_csv(stock_amount_temp_path, index=False, encoding='utf8')

	except:
		stock_log.error(traceback.print_exc())
