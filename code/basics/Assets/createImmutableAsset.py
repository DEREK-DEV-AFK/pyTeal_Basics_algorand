from distutils.log import error
import json
from algosdk import account, transaction, mnemonic
from algosdk.v2client import algod
#from ....details import accounts 

# implementing json 
 # opening file
try: 
    f = open('accounts.json')
    data = json.load(f)

except Exception as error :
    print("no such filee !!") 



# sender details
pv_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
public_address = account.address_from_private_key(pv_key)