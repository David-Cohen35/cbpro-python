from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import time
from collections import defaultdict 

import account
from buys import Buys
import logger
from price_data import Price
import sells
  
def create_values_list():
  values = Price(prices=[],size=0)
  return values

def create_fills_dict():
  fills = Buys(price_bought=dict(),holds=set())
  return fills

def sequence(ticker):
  values = create_values_list()
  fills = create_fills_dict()
  while True:
    Buys.current_price_is_target_buy_price(values,ticker,fills)
    sells.current_price_is_target_sell_price(values,ticker,fills)
    time.sleep(1)
sequence('ETH-USD')