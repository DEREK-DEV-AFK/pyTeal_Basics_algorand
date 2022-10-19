from algosdk.v2client import algod
from algosdk import account, transaction
#from ..Utilites.wait_forConformation import wait_for_confirmation # importing helper files 

# account details
account_private_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
account_public_key = account.address_from_private_key(account_private_key)
print("address", account_public_key)


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


algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2JGwhfPGD03FnmVd9lKzC9oSCexWXM8I8yg1EW9G"
headers = {
    "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)


params = algod_client.suggested_params()

gh = params.gh
first_valid_round = params.first
last_valid_round = params.last
fee = params.min_fee
send_amount = 1

existing_account = account_public_key
send_to_address = "LDGUF6ZQKGFTODZXU37XGR5DEPCCQSJMZ7ZHEKNA6647GI6T2NQ7RDVHFE"

# Create and sign transaction
tx = transaction.PaymentTxn(existing_account, fee, first_valid_round, last_valid_round, gh, send_to_address, send_amount, flat_fee=True)
signed_tx = tx.sign(account_private_key)

try:
    algod_client.send_transaction(signed_tx)
    print('Transaction send with transaction Hash (ID)', signed_tx.transaction.get_txid())
    # 
except Exception as e:
    print('Error',e)