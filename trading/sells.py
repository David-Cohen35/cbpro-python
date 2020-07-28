import bot
import buys
import logger
import price_data

class Sells:
  def target_sell_price(ticker):
    target = str(Price.two_dec(1.007 * Price.midline(ticker)))
    return target

  def determine_limit_sell_price(ticker):#,buy_cost,leeway
    target = str(Price.two_dec(1.012 * Price.midline(ticker)))
    return target
  
  open_sell_orders = {} # make sure there arent global variables like this
  def sell_limit(ticker):#,leeway
    logging.info(auth_client.place_limit_order(product_id=ticker,side='sell',price=determine_limit_sell_price(ticker),size=(ETH_balance)))
    # auth_client.place_limit_order(product_id=ticker,
    #                             side='sell', 
    #                             price=determine_limit_sell_price(ticker),
    #                             size=(ETH_balance))

    # open_sell_orders[(auth_client.place_limit_order(product_id=ticker, '''if creating a leeway for chasing'''
    #                             side='sell', 
    #                             price=determine_limit_sell_price(ticker), #,leeway
    #                             size=(ETH_account['balance'])))['id']] = 5#determine_limit_sell_price(ticker,buy_cost)#,leeway

  def sell_market(ticker, amount):
    auth_client.place_market_order(product_id=ticker, 
                                  side='sell', 
                                  funds=str(amount))

  # def replace_sell_order(order_id,leeway,ticker):
  #   price = two_dec(float(open_sell_orders[order_id])) - 0.01
  #   auth_client.cancel_order(order_id)
  #   sell_limit(ticker, leeway)

  # def chase_bid(ticker, leeway):
  #   if not open_sell_orders:
  #     return
  #   for order_id, open_sell_price in open_sell_orders:
  #     if (open_sell_price - 0.01) > get_bid(ticker): 
  #       if ( open_sell_price - get_bid(ticker) ) < leeway:
  #         return replace_sell_order(order_id,( open_sell_price - get_bid(ticker) ) + 0.01,ticker)
