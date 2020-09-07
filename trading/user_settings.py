import account
import logger

class User:
	def __init__(self,currency,default_buy_cost,default_limit_buy_size,stop_order_percent):
		self.currency = input('Enter BTC or ETH to trade against USD:  ')
		self.default_buy_cost = float(input('Enter $ amount to spend on each market buy order:  '))
		self.default_limit_buy_size = input('Enter amount of crypto to purchase on each limit buy order (minimum "0.01"):  ')
		self.stop_order_percent = input('Enter how many percent below buy price the stop orders should be set:  ')

	# def intake_currency():
	# 	try:
	# 		response = input('Enter BTC or ETH to trade against USD:  ')
	# 		type(response) == str() and (response.upper() == 'ETH' or response.upper() == 'BTC')
	# 	except:
	# 		print('Please enter "BTC" or "ETH"')
	# 		intake_currency()
	
	# def intake_default_buy_cost():
	# 	pass
	
	# def intake_default_limit_buy_size():
	# 	pass

	# def intake_stop_order_percent():
	# 	pass

	def exchange_minimum_amount_for_lowest_market_order_fee():
		return float(50000)

	def at_least_minimum_market_cost(cost):
		return cost if cost>=5 else 5

	def default_buy_cost(inputs):
		return inputs.default_buy_cost

	def default_limit_buy_size():
		return inputs.default_limit_buy_size

	def buy_cost_is_below_exchange_minimum_fee(values,ticker,fills,inputs):
		if float(User.default_buy_cost(inputs)) < User.exchange_minimum_amount_for_lowest_market_order_fee():
			return True
		return False

	def default_stop_order_percent_below_buy_price(price):
		percent_of_whole = (100 - inputs.stop_order_percent) / 100
		response = round(float(price * percent_of_whole),2)
		return response

	def sell_cost_is_below_exchange_minimum_fee(sell_cost):
		if sell_cost < User.exchange_minimum_amount_for_lowest_market_order_fee():
			return True
		return False