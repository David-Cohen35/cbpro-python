import cbpro
import logger
import os
from price_data import Price
import account

def target_buy_price(values,ticker):
  target = str(Price.two_dec(1.00 * Price.midline(values,ticker)))
  return target

def determine_limit_buy_price(values,ticker):
  target = str(Price.two_dec(1.0003 * Price.midline(values,ticker)))
  return target

def buy_limit(values,ticker):
  logger.logging.info("limit buy")
  logger.logging.info(account.auth_client.place_limit_order(product_id=ticker, 
                              side='buy', 
                              price=determine_limit_buy_price(values,ticker),
                              size='1.00'))

def buy_market(ticker, amount):
  logger.logging.info("market buy")
  logger.logging.info(account.auth_client.place_market_order(product_id=ticker, 
                                side='buy', 
                                funds=str(amount)))