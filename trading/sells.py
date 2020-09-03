import account
from buys import Buys
import cbpro
import logger
from price_data import Price
import user_settings

def determine_limit_sell_price(min_sell_price):
  limit_price = str(min_sell_price + 0.01)
  return limit_price

def market_or_limit(ticker,amount,fills,min_sell_cost,k):
  if user_settings.sell_cost_is_below_exchange_minimum_fee(min_sell_cost):
    sell_market(ticker,amount,fills,k)
  else:
    sell_limit(ticker,amount,fills,k)

def check_fills_for_sells(values,ticker,fills,curr_price):
  for k,v in fills.price_bought.items():
    amount = v[0]
    min_sell_price = v[1]
    stop_price = v[2]
    min_sell_cost = round(float(amount) * float(min_sell_price),2)
    if curr_price >= min_sell_price or curr_price <= stop_price:
      market_or_limit(values,ticker,amount,fills,min_sell_cost,k,min_sell_price)
      break
      
def current_price_is_target_sell_price(values,ticker,fills):
  curr_price = Price.get_bid(ticker)
  check_fills_for_sells(values,ticker,fills,curr_price)

def sell_limit(ticker,amount,fills,bought_price,min_sell_price):
  logger.logging.info("setting limit sell order...")
  logger.logging.info(account.auth_client.place_limit_order(product_id=ticker,
                                    side='sell',
                                    price=determine_limit_sell_price(min_sell_price),
                                    size=amount))
  Buys.remove_from_fills_and_holds(fills,bought_price)

def sell_market(ticker,amount,fills,bought_price):
  logger.logging.info("market selling...")
  logger.logging.info(account.auth_client.place_market_order(product_id=ticker,
                                    side='sell',
                                    size=str(amount)))
  Buys.remove_from_fills_and_holds(fills,bought_price)
