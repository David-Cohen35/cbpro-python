import account
from datetime import time
import logger
import math
import statistics

class Price:
  def __init__(self,prices,size,time_keeper):
    self.prices = prices
    self.size = size
    self.time_keeper = time_keeper
  
  def add_to_values(values,num):
    values.prices.append(num)
    values.size += 1
  
  def add_to_time_keeper(values):
    values.time_keeper += 1

  def restart_time_keeper(values):
    values.time_keeper = 0

  def remove_and_add_to_values(values,num):
    values.prices.pop(0)
    values.prices.append(num)

  def price_midline(price_list):
    avg = statistics.median(price_list)
    mid = round(avg,2)
    return mid

  def get_ask(ticker):
    current_orderbook_data = account.auth_client.get_product_order_book(ticker)['asks']
    current_ask_data = current_orderbook_data[0]
    current_ask_price = float(current_ask_data[0])
    return current_ask_price

  def get_bid(ticker):
    current_orderbook_data = account.auth_client.get_product_order_book(ticker)['bids']
    current_bid_data = current_orderbook_data[0]
    current_bid_price = float(current_bid_data[0])
    return current_bid_price

  def midline(values,ticker,inputs):
    if values.size < inputs.mid_size and values.time_keeper == 60:
      Price.add_to_values(values,Price.get_ask(ticker))
      Price.restart_time_keeper(values)
    elif values.size == inputs.mid_size and values.time_keeper == 60:
      Price.remove_and_add_to_values(values,Price.get_ask(ticker))
      Price.restart_time_keeper(values)
    mid = Price.price_midline(values.prices)
    return mid