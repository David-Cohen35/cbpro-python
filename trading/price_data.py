import buys
import cbpro
import logger
import os
import pdb
import sells
import account

class Price:#prices is not avaliable outside of the midline function (line 45)
  def __init__(self,prices,size):
    self.prices = prices
    self.size = size
  
  def add_to_prices(num):
    print(prices)
    print(prices.prices,prices.size,'attributes')
    prices.prices.append(num)
    prices.size += 1
    print(prices.prices,prices.size,'attributes')

  def remove_and_add_to_prices(num):
    prices.prices.pop(0)
    prices.prices.append(num)

  def price_midline(price_list):
    avg = statistics.mean(price_list)
    mid = two_dec(avg)
    return mid

  def get_ask(ticker):
    current_orderbook_data = account.auth_client.get_product_order_book(ticker)['asks']
    current_ask_data = current_orderbook_data[0]
    current_ask_price = float(current_ask_data[0])
    return current_ask_price

  def get_bid(ticker):
    current_orderbook_data = auth_client.get_product_order_book(ticker)['bids']
    current_bid_data = current_orderbook_data[0]
    current_bid_price = float(current_bid_data[0])
    return current_bid_price

  def two_dec(self,num):
    return (math.ceil(num*100)/100)

  def midline(ticker):
    prices = Price(prices=[],size=0)
    print(prices,prices.prices,prices.size,"at creation")
    if prices.size < 59:
      Price.add_to_prices(Price.get_ask(ticker))
    else:
      Price.remove_and_add_to_prices(Price.get_ask(ticker))
    mid = Price.price_midline(prices.prices)
    return mid