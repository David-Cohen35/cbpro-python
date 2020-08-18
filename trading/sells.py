import cbpro
import logger
from price_data import Price
import account

def target_sell_price(values,ticker):
  target = str(Price.two_dec(1.007 * Price.midline(values,ticker)))
  return target

def determine_limit_sell_price(values,ticker):
  target = str(Price.two_dec(1.012 * Price.midline(values,ticker)))
  return target

def sell_limit(values,ticker):
  logger.logging.info("sell limit placed")
  logger.logging.info(account.auth_client.place_limit_order(product_id=ticker, 
                              side='sell', 
                              price=determine_limit_sell_price(values,ticker),
                              size=account.ETH_balance))

def sell_market(ticker, amount):
  logger.logging.info("market selling")
  logger.logging.info(account.auth_client.place_market_order(product_id=ticker, 
                                side='sell', 
                                funds=str(amount)))