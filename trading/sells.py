import account
import cbpro
import logger
from price_data import Price
import user_settings

def target_sell_price(values,ticker):
  target = str(Price.two_dec(1.007 * Price.midline(values,ticker)))
  return target

def determine_limit_sell_price(values,ticker):
  target = str(Price.two_dec(1.012 * Price.midline(values,ticker)))
  return target

def current_price_is_target_sell_price(values,ticker):
  if Price.get_bid(ticker) == float(target_sell_price(values,ticker)):
    user_settings.sell_cost_is_below_exchange_minimum_fee_structure(values, ticker)

def sell_limit(values,ticker,amt_selling):
  if not (float(account.ETH_balance) < 0.01):
    logger.logging.info(account.auth_client.place_limit_order(product_id=ticker,side='sell', price=determine_limit_sell_price(values,ticker),size=amt_selling))
    logger.logging.info("sell limit placed")

def sell_market(ticker, amount):
  logger.logging.info(account.auth_client.place_market_order(product_id=ticker,side='sell',funds=str(amount)))
  logger.logging.info("market sold")