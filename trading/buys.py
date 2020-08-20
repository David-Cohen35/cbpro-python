import account
import cbpro
import logger
from price_data import Price
import sells
import user_settings

def remove_from_fills():
  recent_fills.pop(0)

recent_fills = list()
def empty_fills():
  recent_fills = list()

def maintain_recent_fills(values,ticker):
  if len(recent_fills) > 4:
    recent_fills.pop(0)
  recent_fills.append(target_buy_price(values,ticker))

def target_buy_price(values,ticker):
  target = str(Price.two_dec(1.00 * Price.midline(values,ticker)))
  return target

def determine_limit_buy_price(values,ticker):
  target = str(Price.two_dec(1.0003 * Price.midline(values,ticker)))
  return target

def current_price_is_target_buy_price(values,ticker):
  if Price.get_ask(ticker) == float(target_buy_price(values,ticker)):
    user_settings.buy_cost_is_below_exchange_minimum_fee_structure(values,ticker)

def check_if_buy(values,ticker,cost):
  if target_buy_price(values,ticker) not in recent_fills and values.size > 59: # 59 will be a user setting input
    maintain_recent_fills(values,ticker)
    buy_market(ticker,cost,values)

def check_recent_buys_before_buying(value,ticker):
  if target_buy_price(values,ticker) not in recent_fills:
    buy_limit(values,ticker)

def buy_limit(values,ticker):
  logger.logging.info(account.auth_client.place_limit_order(product_id=ticker,
                                    side='buy',
                                    price=determine_limit_buy_price(values,ticker),
                                    size='1.00'))
  logger.logging.info("limit buy")

def buy_market(ticker, amount,values):
  if not (float(account.USD_balance) < 5) and target_buy_price(values,ticker) not in recent_fills:
    logger.logging.info(account.auth_client.place_market_order(product_id=ticker,
                                      side='buy',
                                      funds=str(amount)))
    logger.logging.info("market buy")
    sells.sell_limit(values,ticker,user_settings.default_sell_amount())