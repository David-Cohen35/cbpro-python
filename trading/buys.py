import account
import cbpro
import logger
from price_data import Price
import user_settings
import time

class Buys:
  def __init__(self,price_bought,holds):
    self.price_bought = price_bought
    self.holds = holds

  def target_buy_price(values,ticker):
    target = str(round((0.998 * Price.midline(values,ticker)),2))
    return target

  def determine_limit_buy_price(values,ticker):
    target = round(0.998 * Price.midline(values,ticker),2)
    target -= 0.01
    return str(target)

  def current_price_is_target_buy_price(values,ticker,fills):
    if Price.get_ask(ticker) <= float(Buys.target_buy_price(values,ticker)):
      if user_settings.buy_cost_is_below_exchange_minimum_fee(values,ticker,fills):
        initialCost = user_settings.default_buy_cost() 
        cost = user_settings.at_least_minimum_market_cost(initialCost)
        Buys.check_if_market_buy(values,ticker,cost,fills)
      else:
        Buys.check_recent_buys_before_limit_buy(values,ticker,fills)

  def check_if_market_buy(values,ticker,cost,fills):
    if str(float(Buys.target_buy_price(values,ticker))//1) not in fills.holds and values.size > 499: #will be a user setting input
      Buys.buy_market(ticker,cost,values,fills)

  def check_recent_buys_before_limit_buy(values,ticker,fills):
    if str(float(target_buy_price(values,ticker))//1) not in fills.holds:
      buy_limit(values,ticker)

  def remove_from_fills_and_holds(fills,bought_price):
    del fills.price_bought[bought_price]
    fills.holds.remove((float(bought_price)//1))

  def buy_limit(values,ticker,fills):
    order_details = account.auth_client.place_limit_order(product_id=ticker,
                                      side='buy',
                                      price=determine_limit_buy_price(values,ticker),
                                      size=user_settings.default_limit_buy_size())
    logger.logging.info(order_details)
    size = user_settings.default_limit_buy_size() 
    price = determine_limit_buy_price(values,ticker)
    fills.price_bought[price] = size
    fills.holds.add((float(price)//1))

  def buy_market(ticker,amount,values,fills):
    if not ((float(account.USD_balance)) < 5) and (float(Buys.target_buy_price(values,ticker))//1) not in fills.holds:
      order_details = account.auth_client.place_market_order(product_id=ticker,
                                        side='buy',
                                        funds=str(amount))
      try:
        size = (float(order_details['funds']) / float(Buys.target_buy_price(values,ticker)))
        size = str(round(size,7))
        price = float(Buys.target_buy_price(values,ticker))
        min_sell_price = round((price*1.01),2)
        fills.price_bought[price] = [size,min_sell_price]
        fills.holds.add((float(price)//1))
        logger.logging.info((fills.price_bought))
        logger.logging.info((fills.holds))
      except:
        pass