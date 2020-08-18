from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import time

import account
import buys
import logger
from price_data import Price
import sells


def at_least_minimum_market_cost(cost):
  return cost if cost>=5 else 5
  
def create_values_list():
  values = Price(prices=[],size=0)
  return values

def current_price_is_target_buy_price(values,ticker):
  return Price.get_ask(ticker) == float(buys.target_buy_price(values,ticker))

def current_price_is_target_sell_price(values,ticker):
  return Price.get_bid(ticker) == float(sells.target_sell_price(values,ticker))

def trade_cost_is_below_exchange_minimum_fee_structure():
  return float(account.USD_balance) * 0.10 < float(50000)

def sell_cost_is_below_exchange_minimum_fee_structure():
  return (Price.two_dec(account.ETH_balance) * Price.two_dec(get_bid(ticker))) < float(50000)

def default_buy_cost():
  return Price.two_dec(float(account.USD_balance) * 0.10)

def default_sell_cost():
  return (Price.two_dec(account.ETH_balance) * Price.two_dec(get_bid(ticker)))

def default_sell_amount(): # will be user input
  return Price.two_dec(float(account.ETH_balance) * 1.00)

def sequence(ticker):
  values = create_values_list()
  recent_fills = list()
  while True:
    if current_price_is_target_buy_price(values,ticker):
      if trade_cost_is_below_exchange_minimum_fee_structure():
        initialCost = default_buy_cost()
        cost = at_least_minimum_market_cost(initialCost)
        if buys.target_buy_price(values,ticker) not in recent_fills and values.size > 59: # make file for default values being received from user for trade size/len(M.A) 
          if len(recent_fills) > 4:
            recent_fills.pop(0)
          recent_fills.append(buys.target_buy_price(values,ticker))
          buys.buy_market(ticker,cost)
          sells.sell_limit(values,ticker,default_sell_amount())
      else:
        if buys.target_buy_price(values,ticker) not in recent_fills:
          buys.buy_limit(values,ticker)
    elif current_price_is_target_sell_price(values,ticker):
      if sell_cost_is_below_exchange_minimum_fee_structure():
        sells.sell_market(ticker, default_sell_amount())
        recent_fills = list()
      else:
        sells.sell_limit(values,ticker,str(default_sell_amount()))
        recent_fills = list()
    time.sleep(1)
sequence('ETH-USD')