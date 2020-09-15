import account
import logger

class User:
	def __init__(self,currency,default_buy_cost,default_limit_buy_size,stop_order_percent,minimum_market_order_size,mid_size):
		self.currency = User.intake_currency(self)
		self.default_buy_cost = User.intake_default_buy_cost(self)
		self.default_limit_buy_size = User.intake_default_limit_buy_size(self)
		self.stop_order_percent = User.intake_stop_order_percent(self)
		self.minimum_market_order_size = User.intake_minimum_market_order_size(self)
		self.mid_size = User.intake_mid_size(self)

	def intake_currency(self):
		response = ''
		while response.upper() not in['ETH', 'BTC']:
			try:
				response = input('Enter BTC or ETH to trade against USD:   ')
				response = response.upper()
			except KeyboardInterrupt:
				print("user wants to quit")
				break
			print("got", response)
		return response

	def intake_default_buy_cost(self):
		response = 0
		while response < 5:
			try:
				response = float(input('Enter $ amount to spend on each market buy order (minimum = 5):   '))
				if response > 5: continue 
			except KeyboardInterrupt:
				print("user wants to quit")
				break
			except:
				print('Must enter a number greater than or equal to 5')
				continue
			print("got", response)
		return response
	
	def intake_default_limit_buy_size(self):
		response = 0.00
		while response < 0.01:
			try:
				response = float(input('Enter amount of crypto to purchase on each limit buy order (minimum "0.01"):  '))
			except KeyboardInterrupt:
				print("user wants to quit")
				break
			except:
				print("Must enter a number greater than or equal to 0.01")
				response = 0.00
				continue
			print("got", response)
		return str(response)

	def intake_stop_order_percent(self):
		response = 0
		while response == 0:
			try:
				response = float(input('Enter how many percent below buy price the stop orders should be set (a number between 0.01-100):  '))
			except KeyboardInterrupt:
				print("user wants to quit")
				break
			except:
				print("Must enter a number between 0-100")
				response = 0
				continue
			print("got", response)
		return response

	def intake_mid_size(self):
		hours = minutes = '0'
		while hours == '0' or minutes == '0':
			try:
				hours = int(input('Enter how many hours in the trading range:  '))
				minutes = int(input('Enter how many minutes in the trading range:  '))
				response = (hours * 60) + minutes
				if response < 1: hours = minutes = '0'
			except KeyboardInterrupt:
				print("user wants to quit")
				break
			except:
				print("Must enter a whole number greater than or equal to 0")
				hours = minutes = '0'
				continue
			print("got", hours,"hour(s) and", minutes,"minutes")
		return response

	def intake_minimum_market_order_size(self):
		return 50000.00

	def at_least_minimum_market_cost(cost):
		return cost if cost>=5 else 5

	def default_buy_cost(inputs):
		return inputs.default_buy_cost

	def default_limit_buy_size():
		return inputs.default_limit_buy_size

	def buy_cost_is_below_exchange_minimum_fee(values,ticker,fills,inputs):
		if inputs.default_buy_cost < inputs.minimum_market_order_size:
			return True
		return False

	def default_stop_order_percent_below_buy_price(price,inputs):
		percent_of_whole = (100 - inputs.stop_order_percent) / 100
		response = round(float(price * percent_of_whole),2)
		return response

	def sell_cost_is_below_exchange_minimum_fee(sell_cost):
		if sell_cost < 50000.00:
			return True
		return False
