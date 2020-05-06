import traceback
import log
import os
import pandas
import shopee.config as config

conf = config.get_config()
stock_log = log.get_logger(logger_name="lib.resource.stock", logging_level=conf.get("LOGGING", "LEVEL"))
stock_amount_file_path = "{}/input_file/stock_amount.csv".format(os.path.dirname(os.path.realpath(__file__)))

def get_stock_amount():
	if os.path.exists(stock_amount_file_path):
		try:
			df_header = pandas.read_csv(stock_amount_file_path, nrows=1)
			df_header_list = list(df_header.columns)
			df_stock_amount = pandas.read_csv(stock_amount_file_path, \
				names=df_header_list, usecols=df_header_list, skiprows=1, keep_default_na=False)
			stock_amount_list = []

			for i in df_stock_amount.index:
				ommohome_product = str(df_stock_amount.loc[i, 'ommohome_product'])
				shopee_product = str(df_stock_amount.loc[i, 'shopee_product'])
				variation_type = str(df_stock_amount.loc[i, 'variation_type'])
				variation_data = str(df_stock_amount.loc[i, 'variation_data'])
				previous_amount = str(df_stock_amount.loc[i, 'previous_amount'])
				current_amount = str(df_stock_amount.loc[i, 'current_amount'])

				stock_amount_list.append([
					ommohome_product, 
					shopee_product, 
					variation_type, 
					variation_data, 
					previous_amount,
					current_amount
				])

			stock_log.info("Successfully retrieved stock amount")

		except:
			stock_log.error(traceback.print_exc())
	else:
		stock_log.error("Invalid path for stock amount file : {}".format(stock_amount_file_path))

	return stock_amount_list
