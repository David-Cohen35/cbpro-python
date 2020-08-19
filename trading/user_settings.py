import account
import buys
from price_data import Price
import sells

def at_least_minimum_market_cost(cost):
	return cost if cost>=5 else 5

def default_buy_cost():
	return Price.two_dec(float(account.USD_balance) * 0.10)

def default_sell_amount():
	return Price.two_dec(float(account.ETH_balance) * 1.00)

def buy_cost_is_below_exchange_minimum_fee_structure(values,ticker):
	if (float(account.USD_balance) * 0.10) < float(50000):
		initialCost = default_buy_cost() 
		cost = at_least_minimum_market_cost(initialCost)
		buys.check_if_buy(values,ticker,cost)
	else:
		buys.check_recent_buys_before_buying(values,ticker)

def sell_cost_is_below_exchange_minimum_fee_structure(values, ticker):
	if (Price.two_dec(account.ETH_balance) * Price.two_dec(get_bid(ticker))) < float(50000):
		sells.sell_market(ticker,default_sell_amount())
		buys.empty_fills()
	else:
		sells.sell_limit(values,ticker,str(default_sell_amount()))
		buys.empty_fills()