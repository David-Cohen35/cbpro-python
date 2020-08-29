import cbpro
import os


auth_client = cbpro.AuthenticatedClient(key=os.getenv("key"), b64secret=os.getenv("b64secret"), passphrase=os.getenv("passphrase"))
usd_account=os.getenv("usd_account")
USD_account = auth_client.get_account(usd_account)
eth_account=os.getenv("eth_account")
ETH_account = auth_client.get_account(eth_account)
ETH_balance = str(ETH_account['available'])
USD_balance = str(USD_account['available'])