import cbpro
import os


auth_client = cbpro.AuthenticatedClient(key=os.getenv("key"), b64secret=os.getenv("b64secret"), passphrase=os.getenv("passphrase"))
USD_account = (auth_client.get_account('256cc64c-a387-456e-9fe1-87ec139e4d2e'))
ETH_account = (auth_client.get_account('9fbbf4ce-3dc6-4611-90d8-b475605caa8f'))
ETH_balance = str(ETH_account['available'])
USD_balance = str(USD_account['available'])
