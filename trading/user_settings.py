import account
from price_data import Price

def at_least_minimum_market_cost(cost):
	return cost if cost>=5 else 5

def default_buy_cost():
	return round((float(account.USD_balance) * 0.10),2)

def default_limit_buy_size():
	return '0.01'

def buy_cost_is_below_exchange_minimum_fee(values,ticker,fills):
	if (float(account.USD_balance) * 0.10) < float(50000):# default_buy_cost < float(50000)
		return True
	else:
		return False

def sell_cost_is_below_exchange_minimum_fee(amount,values,ticker,fills):
	if round(float(amount) * float(Price.get_bid(ticker)),2) < float(50000):
		return True
	else:
		return False