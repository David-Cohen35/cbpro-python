import cbpro
import logger
from price_data import Price
import account

def target_buy_price(values,ticker):
  target = str(Price.two_dec(1.00 * Price.midline(values,ticker)))
  return target

def determine_limit_buy_price(values,ticker):
  target = str(Price.two_dec(1.0003 * Price.midline(values,ticker)))
  return target

def buy_limit(values,ticker):
  logger.logging.info(account.auth_client.place_limit_order(product_id=ticker, 
                              side='buy', 
                              price=determine_limit_buy_price(values,ticker),
                              size='1.00'))
  logger.logging.info("limit buy")

def buy_market(ticker, amount):
  if not (float(account.USD_balance) < 5): # if below minimum cost allowed on exchange ( get from user input or default 5 )
    logger.logging.info(account.auth_client.place_market_order(product_id=ticker, 
                                  side='buy', 
                                  funds=str(amount)))
    logger.logging.info("market buy")