import bot
import logger
import price_data
import sells

class Buys:
  def target_buy_price(ticker):
    target = str(Price.two_dec(1.00 * Price.midline(ticker)))
    return target

  def determine_limit_buy_price(ticker):#,leeway
    target = str(Price.two_dec(1.0003 * Price.midline(ticker)))
    return target
  
  open_buy_orders = {} # make sure there arent global variables like this
  def buy_limit(ticker):#, leeway
    logging.info("limit buy")
    open_buy_orders[(auth_client.place_limit_order(product_id=ticker, 
                                side='buy', 
                                price=determine_limit_buy_price(ticker), #,leeway
                                size='1.00'))['id']] = determine_limit_buy_price(ticker)#,leeway
  def buy_market(ticker,cost):
    logging.info(auth_client.place_market_order(product_id=ticker,side='buy',funds=str(cost)))


  # def replace_buy_order(order_id,leeway,ticker):
  #   price = two_dec(float(open_buy_orders[order_id])) + 0.01
  #   auth_client.cancel_order(order_id)
  #   buy_limit(ticker, leeway)

  # def chase_ask(ticker, leeway):
  #   if not open_buy_orders:
  #     return
  #   for order_id, open_buy_price in open_buy_orders:
  #     if (open_buy_price + 0.01) < get_ask(ticker):
  #       if (get_ask(ticker) - open_buy_price) < leeway:
  #         return replace_buy_order(order_id,((get_ask(ticker) - open_buy_price) - 0.01),ticker)
