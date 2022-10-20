from algosdk import transaction, account
from algosdk.v2client import algod

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


# account details
account_private_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
account_public_key = account.address_from_private_key(account_private_key)
send_to= 'LDGUF6ZQKGFTODZXU37XGR5DEPCCQSJMZ7ZHEKNA6647GI6T2NQ7RDVHFE'
send_to_private_key = '43VV/+zG/GPHB74Z4/Wn00Qs65XxpDJ9pMqUWM2mmoZYzUL7MFGLNw83pv9zR6MjxChJLM/ycimg97nzI9PTYQ=='

# creating algod client for sending transaction
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2JGwhfPGD03FnmVd9lKzC9oSCexWXM8I8yg1EW9G"
headers = {
    "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)

params = algod_client.suggested_params()
# transaction parameters
fee = params.min_fee
first_valid_round = params.first
last_valid_round = params.last
genesis_hash = params.gh

asset_id = 117040603

#
# use aassetTransferTxn to send and optin asset
txn = transaction.AssetTransferTxn (
        sender=account_public_key,
        fee=fee,
        first=first_valid_round,
        last=last_valid_round,
        gh=genesis_hash,
        receiver=send_to,
        amt=10,
        index=117040603
    )

signed_txn = txn.sign(account_private_key)

try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txid : ",txid)

    wait_for_confirmation(algod_client,txid)
except Exception as err :
    print(err)