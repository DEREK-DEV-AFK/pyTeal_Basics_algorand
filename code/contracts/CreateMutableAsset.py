# Creating asset

from algosdk import account
from algosdk.future import transaction
from algosdk.v2client import algod

# creator
creator_private_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
creator_address = 'VZVLFSQZPALVXN6UORP5LMEN6KUQ6XEG73YM6UBCZ2RUZP4N57GMUAZ4SU'

# account that can freeze others account for this asset
freezer_private_key = '43VV/+zG/GPHB74Z4/Wn00Qs65XxpDJ9pMqUWM2mmoZYzUL7MFGLNw83pv9zR6MjxChJLM/ycimg97nzI9PTYQ=='
freezer_address = 'LDGUF6ZQKGFTODZXU37XGR5DEPCCQSJMZ7ZHEKNA6647GI6T2NQ7RDVHFE'

# account able to update asset configuration
manager_private_key = 'iA0ajPTJjNREPGu0a0qDnWq5B4bcMbQdTNMEb14U+dMQ6Np3j0NIWh9aijM3P3e2NtzEfj7WMGNb7HXxxgN4KA=='
manager_address = 'CDUNU54PINEFUH22RIZTOP3XWY3NZRD6H3LDAY235R27DRQDPAUKCTQTTI'

# account allowed to take this asset from other account
clawer_private_key = 'yPgFy8TQqcKjC9ZTVHJo95WZzsPhProxozWcnNsYismPjVBYFKAh4hO3woZf9rKy7xgJVp4t31GpWNog3yBfWQ=='
clawer_address = 'R6GVAWAUUAQ6EE5XYKDF75VSWLXRQCKWTYW56UNJLDNCBXZAL5M6PGLNEI'

# account that holds reservers for this asset
reserver_private_key = 'UmWJxg2G30v/sLqHGS5g845KfbBi7LrCMWsvpefZkc2c0Ti++QlwqyvYZiBNOrznymuEMRqRVQx4mPuTjmjjuQ=='
reserver_address = 'TTITRPXZBFYKWK6YMYQE2OV447FGXBBRDKIVKDDYTD5ZHDTI4O466NPMT4'

# creating client to send tx to network

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2JGwhfPGD03FnmVd9lKzC9oSCexWXM8I8yg1EW9G"
headers = {
    "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers) # algod client created here

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo


params = algod_client.suggested_params()
print('Suggested parameters')
print(params)

# transaction parameters
fee = params.min_fee
first_valid_round = params.first
last_valid_round = params.last
genesis_hash = params.gh

# asset parameters
totalSupply = 100  # max supply of this set
assetName = "derekCoin" # name of asset
unitName = 'Dcoin' # symbol of asset
asseturl = 'https://github.com/DEREK-DEV-AFK' # link to your asset docs or any other page related to your asset
default_frozen = False # wheather account should be frozen by default 

# create the asset creation transaction
sp = transaction.SuggestedParams(fee,first_valid_round,last_valid_round,genesis_hash)

txn = transaction.AssetCreateTxn(
    sender=creator_address,
    sp=sp,
    total=totalSupply,
    decimals=0,
    default_frozen=False,
    manager=manager_address,
    reserve=reserver_address,
    freeze=freezer_address,
    clawback=clawer_address,
    unit_name=unitName,
    asset_name=assetName,
    url=asseturl,
)

# sign tx
signed_txn = txn.sign(creator_private_key)



try:
    # sending transaction 
    algod_client.send_transaction(signed_txn)
    # printing transaction hash
    print('Transaction send with transaction Hash (ID)', signed_txn.transaction.get_txid())
    wait_for_confirmation(algod_client, txid=signed_txn.transaction.get_txid())
except Exception as e:
    # if any error occurrs it will log error
    print('Error',e)
