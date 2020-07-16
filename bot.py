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

logging.basicConfig(filename='/Users/davidcohen/Desktop/cbpro-python/app.log'.format(time.time()),
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

logger = logging.getLogger(__name__)

logging.debug("a")
logging.info("b")
logging.warning("c")
logging.error("d")
logging.critical("e")

auth_client = cbpro.AuthenticatedClient(key=os.getenv("key"), b64secret=os.getenv("b64secret"), passphrase=os.getenv("passphrase"))

USD_account = (auth_client.get_account('256cc64c-a387-456e-9fe1-87ec139e4d2e'))
ETH_account = (auth_client.get_account('9fbbf4ce-3dc6-4611-90d8-b475605caa8f'))

ETH_balance = str(ETH_account['available'])
USD_balance = str(USD_account['available'])

def get_ask(ticker):
  current_orderbook_data = auth_client.get_product_order_book('ETH-USD')['asks']
  current_ask_data = current_orderbook_data[0]
  current_ask_price = float(current_ask_data[0])
  return current_ask_price

def get_bid(ticker):
  current_orderbook_data = auth_client.get_product_order_book('ETH-USD')['bids']
  current_bid_data = current_orderbook_data[0]
  current_bid_price = float(current_bid_data[0])
  return current_bid_price

def two_dec(num):
  return (math.ceil(num*100)/100)

prices = [] # make sure there arent global variables like this
def midline(ticker):
  if (len(prices) < 60):
    prices.append(get_ask(ticker))
  else:
    prices.pop(0)
    prices.append(get_ask(ticker))
  avg = statistics.mean(prices)
  price_midline = two_dec(avg)
  return price_midline

def target_buy_price(ticker):
  target = two_dec(1.00 * midline(ticker))
  return target

def target_sell_price(ticker):
  target = two_dec(1.007 * midline(ticker))
  # print(target, "sell price")
  return target

def determine_limit_buy_price(ticker):#,leeway
  target = str(two_dec(1.0003 * midline(ticker))  )
  return target
  
def determine_limit_sell_price(ticker):#,buy_cost,leeway
  target = str(two_dec(1.012 * midline(ticker)))
  return target
 
open_buy_orders = {} # make sure there arent global variables like this
def buy_limit(ticker):#, leeway
  logging.info("limit buy")
  open_buy_orders[(auth_client.place_limit_order(product_id=ticker, 
                              side='buy', 
                              price=determine_limit_buy_price(ticker), #,leeway
                              size='1.00'))['id']] = determine_limit_buy_price(ticker)#,leeway

open_sell_orders = {} # make sure there arent global variables like this
def sell_limit(ticker):#,leeway
  logging.info(auth_client.place_limit_order(product_id=ticker,side='sell',price=determine_limit_sell_price(ticker),size=(ETH_balance)))
  # auth_client.place_limit_order(product_id=ticker,
  #                             side='sell', 
  #                             price=determine_limit_sell_price(ticker),
  #                             size=(ETH_balance))

  # open_sell_orders[(auth_client.place_limit_order(product_id=ticker, '''if creating a leeway for chasing'''
  #                             side='sell', 
  #                             price=determine_limit_sell_price(ticker), #,leeway
  #                             size=(ETH_account['balance'])))['id']] = 5#determine_limit_sell_price(ticker,buy_cost)#,leeway
  

def buy_market(ticker,cost):
  logging.info(auth_client.place_market_order(product_id=ticker,side='buy',funds=str(cost)))

def sell_market(ticker, amount):
  auth_client.place_market_order(product_id=ticker, 
                                side='sell', 
                                funds=str(amount))


# def replace_buy_order(order_id,leeway,ticker):
#   price = two_dec(float(open_buy_orders[order_id])) + 0.01
#   auth_client.cancel_order(order_id)
#   buy_limit(ticker, leeway)

# def replace_sell_order(order_id,leeway,ticker):
#   price = two_dec(float(open_sell_orders[order_id])) - 0.01
#   auth_client.cancel_order(order_id)
#   sell_limit(ticker, leeway)


# def chase_ask(ticker, leeway):
#   if not open_buy_orders:
#     return
#   for order_id, open_buy_price in open_buy_orders:
#     if (open_buy_price + 0.01) < get_ask(ticker):
#       if (get_ask(ticker) - open_buy_price) < leeway:
#         return replace_buy_order(order_id,((get_ask(ticker) - open_buy_price) - 0.01),ticker)
    
# def chase_bid(ticker, leeway):
#   if not open_sell_orders:
#     return
#   for order_id, open_sell_price in open_sell_orders:
#     if (open_sell_price - 0.01) > get_bid(ticker): 
#       if ( open_sell_price - get_bid(ticker) ) < leeway:
#         return replace_sell_order(order_id,( open_sell_price - get_bid(ticker) ) + 0.01,ticker)

def at_least_minimum_market_cost(cost):
  if cost >= 5:
    return cost
  else:
    return 5

def engine(ticker):#, leeway     break this up into more methods
  recent_fills = []
  while True: # it doesnt realtime update my wallet 
    midline(ticker)
    # chase_ask(ticker, leeway)
    # chase_bid(ticker, leeway)
    if get_ask(ticker) == float(target_buy_price(ticker)):
      if float(USD_balance) * 0.10 < float(50000):
        initialCost = two_dec(float(USD_balance) * 0.10)
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
    if get_bid(ticker) == target_sell_price(ticker):
      if (two_dec(ETH_balance) * two_dec(get_bid(ticker))) < float(50000):
        amt_selling = two_dec(float(ETH_balance) * 1.00)
        sell_market(ticker, amt_selling)
        recent_fills = []
      else:
        sell_limit(ticker)#,buy_cost,leeway
        recent_fills = []
    time.sleep(1)
engine('ETH-USD')#, 0.05


#check if leeway needs to be a string
# auth_client.place_stop_order(product_id='ETH-USD', 
#                               side='buy', 
#                               price='220.00', 
#                               size='0.01')
                              
# auth_client.cancel_all(product_id='ETH-USD')