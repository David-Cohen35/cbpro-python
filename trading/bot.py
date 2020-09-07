from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import time
from collections import defaultdict 

import account
from buys import Buys
import logger
from price_data import Price
import sells
from user_settings import User

def create_values_list():
  values = Price(prices=[0],size=0,time_keeper=0)
  return values

def create_fills_dict():
  fills = Buys(price_bought=dict(),holds=set())
  return fills

def get_users_input():
  inputs = User(currency=str(),default_buy_cost=int(),default_limit_buy_size=str(),stop_order_percent=int())
  return inputs

inputs = get_users_input()
def sequence(inputs,ticker):
  values = create_values_list()
  fills = create_fills_dict()
  while True:
    Buys.current_price_is_target_buy_price(values,ticker,fills,inputs)
    sells.current_price_is_target_sell_price(values,ticker,fills)
    values.time_keeper += 1
    time.sleep(1)
chosen_currency = f'{(inputs.currency).upper()}-USD'
sequence(inputs,chosen_currency)