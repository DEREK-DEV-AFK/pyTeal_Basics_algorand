import json
from algosdk import transaction, account
from algosdk.v2client import algod

# account details
account_private_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
account_public_key = account.address_from_private_key(account_private_key)

# transaction waiting function 
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


#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break



# creating algod client for sending transaction
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2JGwhfPGD03FnmVd9lKzC9oSCexWXM8I8yg1EW9G"
headers = {
    "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)

# OPT-IN
# Check if asset_id is in accounts asset holdings prior
# to opt-in
params = algod_client.suggested_params()

# transaction parameters
fee = params.min_fee
first_valid_round = params.first
last_valid_round = params.last
genesis_hash = params.gh

#sp = transaction.SuggestedParams(fee,first_valid_round,last_valid_round,genesis_hash)

# check if the user has opted it or not
account_info = algod_client.account_info(account_public_key)
holding = None
idx = 0
asset_id = 117040603

for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

# if not holding 

if not holding:
    # use aassetTransferTxn to send and optin asset
    txn = transaction.AssetTransferTxn (
        sender=account_public_key,
        fee=fee,
        first=first_valid_round,
        last=last_valid_round,
        gh=genesis_hash,
        receiver=account_public_key,
        amt=0,
        index=117040603
    )

    signed_txn = txn.sign(account_private_key)

    try:
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txid : {}".txid)

        wait_for_confirmation(algod_client,txid)
    except Exception as err :
        print(err)

   
   # print asset holdings
   #print_asset_holding(algod_client,account_public_key, 117040603)