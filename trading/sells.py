import cbpro
import logger
import os
import price_data
import account

class Sells:
  def target_sell_price(ticker):
    target = str(Price.two_dec(1.007 * Price.midline(ticker)))
    return target

  def determine_limit_sell_price(ticker):#,buy_cost,leeway
    target = str(Price.two_dec(1.012 * Price.midline(ticker)))
    return target
  
  open_sell_orders = {} 
  def sell_limit(ticker):
    logging.info(account.auth_client.place_limit_order(
      product_id=ticker,
      side='sell',
      price=determine_limit_sell_price(ticker),
      size=(ETH_balance)))
    
  def sell_market(ticker, amount):
    account.auth_client.place_market_order(product_id=ticker, 
                                  side='sell', 
                                  funds=str(amount))


    # open_sell_orders[(account.auth_client.place_limit_order(
    #   product_id=ticker,
    #   side='sell', 
    #   price=determine_limit_sell_price(ticker),
    #   size=(ETH_account['balance'])))['id']] = 5 
