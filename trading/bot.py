import cbpro
import datetime
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from itertools import islice
import keyboard
import logging
import math
import os
import pdb
import statistics
import time

import buys
import logger
from price_data import Price
import sells
import account


def at_least_minimum_market_cost(cost):
  if cost >= 5:
    return cost
  else:
    return 5

def sequence(ticker):
  recent_fills = []
  while True: 
    if Price.get_ask(ticker) == float(buys.target_buy_price(ticker)):
      if float(account.USD_balance) * 0.10 < float(50000):
        initialCost = Price.two_dec(float(USD_balance) * 0.10)
        cost = at_least_minimum_market_cost(initialCost)
        if cost not in recent_fills and len(prices) > 59:
          if len(recent_fills) > 4:
            recent_fills.pop(0)
          recent_fills.append(cost)
          buys.buy_market(ticker,cost)
          logging.info(account.ETH_balance)
          Sells.sell_limit(ticker)
      else:
        if cost not in recent_fills:
          buys.buy_limit(ticker)
    if Price.get_bid(ticker) == target_sell_price(ticker):
      if (Price.two_dec(account.ETH_balance) * Price.two_dec(get_bid(ticker))) < float(50000):
        amt_selling = Price.two_dec(float(account.ETH_balance) * 1.00)
        sells.sell_market(ticker, amt_selling)
        recent_fills = []
      else:
        sells.sell_limit(ticker)
        recent_fills = []
    time.sleep(1)
sequence('ETH-USD')