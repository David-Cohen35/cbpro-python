from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import time

import account
import buys
import logger
from price_data import Price
import sells
  
def create_values_list():
  values = Price(prices=[],size=0)
  return values

def sequence(ticker):
  values = create_values_list()
  while True:
    buys.current_price_is_target_buy_price(values,ticker)
    sells.current_price_is_target_sell_price(values,ticker)
    time.sleep(1)
sequence('ETH-USD')