from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import time

import account
import buys
import logger
from price_data import Price
import sells


def at_least_minimum_market_cost(cost):
  if cost >= 5:
    return cost
  else:
    return 5

def sequence(ticker):
  recent_fills = []
  values = Price(prices=[],size=0)
  while True:
    if Price.get_ask(ticker) == float(buys.target_buy_price(values,ticker)):
      if float(account.USD_balance) * 0.10 < float(50000):
        initialCost = Price.two_dec(float(account.USD_balance) * 0.10)
        cost = at_least_minimum_market_cost(initialCost)
        if cost not in recent_fills and values.size > 59:
          if len(recent_fills) > 4:
            recent_fills.pop(0)
          recent_fills.append(cost)
          buys.buy_market(ticker,cost)
          sells.sell_limit(values,ticker)
      else:
        if cost not in recent_fills:
          buys.buy_limit(values,ticker)
    if Price.get_bid(ticker) == float(sells.target_sell_price(values,ticker)):
      if (Price.two_dec(account.ETH_balance) * Price.two_dec(get_bid(ticker))) < float(50000):
        amt_selling = Price.two_dec(float(account.ETH_balance) * 1.00)
        sells.sell_market(ticker, amt_selling)
        recent_fills = []
      else:
        sells.sell_limit(values,ticker)
        recent_fills = []
    time.sleep(1)
sequence('ETH-USD')