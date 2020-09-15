import account
import cbpro
import logger
from price_data import Price
from user_settings import User
import time

class Buys:
  def __init__(self,price_bought,holds):
    self.price_bought = price_bought
    self.holds = holds

  def target_buy_price(values,ticker,inputs):
    target = str(round((0.9995 * Price.midline(values,ticker,inputs)),2))
    return target

  def determine_limit_buy_price(values,ticker,inputs):
    target = round(0.9995 * Price.midline(values,ticker,inputs),2)
    target -= 0.01
    return str(target)

  def market_or_limit(values,ticker,fills,inputs):
    if User.buy_cost_is_below_exchange_minimum_fee(values,ticker,fills,inputs):
        initialCost = User.default_buy_cost(inputs)
        cost = User.at_least_minimum_market_cost(initialCost)
        Buys.check_if_market_buy(values,ticker,cost,fills,inputs)
    else:
      Buys.check_recent_buys_before_limit_buy(values,ticker,fills,inputs)

  def current_price_is_target_buy_price(values,ticker,fills,inputs):
    if Price.get_ask(ticker) <= float(Buys.target_buy_price(values,ticker,inputs)):
      Buys.market_or_limit(values,ticker,fills,inputs)
  
  def check_if_market_buy(values,ticker,cost,fills,inputs):
    curr_target = float(Buys.target_buy_price(values,ticker,inputs))
    if (float(account.USD_balance) >= 5) and ((curr_target//1) not in fills.holds) and (values.size >= inputs.mid_size -1):
      print(curr_target//1,"curr target")
      print(fills.holds,'fills holds')
      print((curr_target//1) not in fills.holds,'curr target is not in fills holds')
      Buys.buy_market(ticker,cost,values,fills,inputs)

  def check_recent_buys_before_limit_buy(values,ticker,fills,inputs):
    curr_target = float(Buys.target_buy_price(values,ticker,inputs))
    if (curr_target//1) not in fills.holds:
      Buys.buy_limit(values,ticker,inputs)
  
  def manage_fills_and_holds(order_details,inputs,fills):
    try:
      order = account.auth_client.get_order(order_details['id'])
      size = order['filled_size']
      price = round((float(order['executed_value']) / float(size)),2)
      min_sell_price = round((price*1.018),2)
      stop_price = User.default_stop_order_percent_below_buy_price(price,inputs)
      fills.price_bought[price] = [size,min_sell_price,stop_price]
      fills.holds.add((price//1))
      fills.holds.add((price//1)+1)
      fills.holds.add((price//1)-1)
      logger.logging.info(order_details)
      logger.logging.info(fills.price_bought)
      logger.logging.info(fills.holds)
    except:
      pass

  def remove_from_fills_and_holds(fills,bought_price):
    bought_price = float(bought_price)
    del fills.price_bought[bought_price]
    fills.holds.remove(bought_price//1)
    fills.holds.remove((bought_price//1)+1)
    fills.holds.remove((bought_price//1)-1)
    logger.logging.info(fills.holds)

  def manage_limit_buy(fills,price,size,order_details):
    fills.price_bought[price] = [size,0,0,0]
    fills.holds.add(float(price)//1)
    logger.logging.info(order_details)

  def buy_limit(values,ticker,fills,inputs):
    order_details = account.auth_client.place_limit_order(product_id=ticker,
                                      side='buy',
                                      price=determine_limit_buy_price(values,ticker,inputs),
                                      size=User.default_limit_buy_size())
    Buys.manage_limit_buy(fills,price,size,order_details)

  def buy_market(ticker,amount,values,fills,inputs):
    order_details = account.auth_client.place_market_order(product_id=ticker,
                                      side='buy',
                                      funds=str(amount))
    Buys.manage_fills_and_holds(order_details,inputs,fills)