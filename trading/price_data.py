import bot
import buys
import logger
import sells

class Price:
  #cant get the price array to work
  def __init__(self):
    self.prices = []

  def get_ask(ticker):
    current_orderbook_data = auth_client.get_product_order_book('ETH-USD')['asks']
    current_ask_data = current_orderbook_data[0]
    current_ask_price = float(current_ask_data[0])
    return current_ask_price

  def get_bid(ticker):
    current_orderbook_data = auth_client.get_product_order_book('ETH-USD')['bids']
    current_bid_data = current_orderbook_data[0]
    current_bid_price = float(current_bid_data[0])
    return current_bid_price

  def two_dec(num):
    return (math.ceil(num*100)/100)

  def midline(ticker):
    #issue with price attribute of Prices
    if (len(Price.prices) < 60):
      Price.prices.append(get_ask(ticker))
    else:
      Price.prices.pop(0)
      Price.prices.append(get_ask(ticker))
    avg = statistics.mean(Price.prices)
    price_midline = two_dec(avg)
    return price_midline