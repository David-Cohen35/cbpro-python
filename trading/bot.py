import cbpro
import time
import datetime
import statistics
import math
from itertools import islice
import os
import keyboard
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import logging, time

import buys
import logger
from price_data import Price
import sells

auth_client = cbpro.AuthenticatedClient(key=os.getenv("key"), b64secret=os.getenv("b64secret"), passphrase=os.getenv("passphrase"))

USD_account = (auth_client.get_account('256cc64c-a387-456e-9fe1-87ec139e4d2e'))
ETH_account = (auth_client.get_account('9fbbf4ce-3dc6-4611-90d8-b475605caa8f'))

ETH_balance = str(ETH_account['available'])
USD_balance = str(USD_account['available'])


def at_least_minimum_market_cost(cost):
  if cost >= 5:
    return cost
  else:
    return 5

def sequence(ticker):#, leeway     break this up into more methods
  recent_fills = []
  while True: # it doesnt realtime update my wallet 
    Price.midline(ticker)
    # chase_ask(ticker, leeway)
    # chase_bid(ticker, leeway)
    if Price.get_ask(ticker) == float(target_buy_price(ticker)):
      if float(USD_balance) * 0.10 < float(50000):
        initialCost = Price.two_dec(float(USD_balance) * 0.10)
        cost = at_least_minimum_market_cost(initialCost)
        if cost not in recent_fills and len(prices) > 59:
          if len(recent_fills) > 4:
            recent_fills.pop(0)
          recent_fills.append(cost)
          buy_market(ticker,cost)
          logging.info(ETH_balance)
          sell_limit(ticker)#cost,leeway
      else:
        if cost not in recent_fills:
          buy_limit(ticker)#, leeway
    if Price.get_bid(ticker) == target_sell_price(ticker):
      if (Price.two_dec(ETH_balance) * Price.two_dec(get_bid(ticker))) < float(50000):
        amt_selling = Price.two_dec(float(ETH_balance) * 1.00)
        sell_market(ticker, amt_selling)
        recent_fills = []
      else:
        sell_limit(ticker)#,buy_cost,leeway
        recent_fills = []
    time.sleep(1)
sequence('ETH-USD')#, 0.05


#check if leeway needs to be a string
# auth_client.place_stop_order(product_id='ETH-USD', 
#                               side='buy', 
#                               price='220.00', 
#                               size='0.01')
                              
# auth_client.cancel_all(product_id='ETH-USD')