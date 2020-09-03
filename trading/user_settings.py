import account
import logger

def currencies():
	return ('ETH-USD')

def exchange_minimum_amount_for_lowest_market_order_fee():
	return float(50000)

def at_least_minimum_market_cost(cost):
	return cost if cost>=5 else 5

def default_buy_cost():
	return 5

def default_limit_buy_size():
	return '0.01'

def buy_cost_is_below_exchange_minimum_fee(values,ticker,fills):
	if default_buy_cost() < exchange_minimum_amount_for_lowest_market_order_fee():
		return True
	return False

def default_stop_order_percent_below_buy_price(price):
	input = 3
	percent_of_whole = (100 - input) / 100
	response = round(float(price * percent_of_whole),2)
	return response 

def sell_cost_is_below_exchange_minimum_fee(sell_cost):
	if sell_cost < exchange_minimum_amount_for_lowest_market_order_fee():
		return True
	return False