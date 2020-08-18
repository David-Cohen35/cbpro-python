import account
import cbpro
import logger
import math
import os
import pdb
import statistics

class Price:
  def __init__(self,prices,size):
    self.prices = prices
    self.size = size
  
  def add_to_values(values,num):
    values.prices.append(num)
    values.size += 1

  def remove_and_add_to_values(values,num):
    values.prices.pop(0)
    values.prices.append(num)

  def price_midline(price_list):
    avg = statistics.mean(price_list)
    mid = Price.two_dec(avg)
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

  def two_dec(num):
    return (math.ceil(num*100)/100)

  def midline(values,ticker):
    if values.size < 60:
      Price.add_to_values(values,Price.get_ask(ticker))
    else:
      Price.remove_and_add_to_values(values,Price.get_ask(ticker))
    mid = Price.price_midline(values.prices)
    return mid