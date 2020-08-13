import cbpro
import logger
import os
from price_data import Price
import account


def target_buy_price(ticker):
  target = str(Price.two_dec(1.00 * Price.midline(ticker)))
  return target
def determine_limit_buy_price(ticker):
  target = str(Price.two_dec(1.0003 * Price.midline(ticker)))
  return target

open_buy_orders = {}
def buy_limit(ticker):
  logging.info("limit buy")
  open_buy_orders[(Bot.account.auth_client.place_limit_order(product_id=ticker, 
                              side='buy', 
                              price=determine_limit_buy_price(ticker), #,leeway
                              size='1.00'))['id']] = determine_limit_buy_price(ticker)#,leeway
def buy_market(ticker,cost):
  logging.info(Bot.account.auth_client.place_market_order(product_id=ticker,side='buy',funds=str(cost)))
