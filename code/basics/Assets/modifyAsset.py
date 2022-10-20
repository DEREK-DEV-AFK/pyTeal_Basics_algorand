# only the manager can modify the parameters(freezer,clawback, manager, reserve) only this can be modify

from algosdk import transaction, account
from algosdk.v2client import algod

# helper functions
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
manager_private_key = 'iA0ajPTJjNREPGu0a0qDnWq5B4bcMbQdTNMEb14U+dMQ6Np3j0NIWh9aijM3P3e2NtzEfj7WMGNb7HXxxgN4KA=='
manager_address = account.address_from_private_key(manager_private_key)

# setting up algod client to interact with network
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "2JGwhfPGD03FnmVd9lKzC9oSCexWXM8I8yg1EW9G"
headers = {
    "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)
 
# getting params 
params = algod_client.suggested_params()

# making transaction
tx = transaction.AssetConfigTxn(
    sender=manager_address,
    fee=params.min_fee,
    first=params.first,
    last=params.last,
    gh=params.gh,
    manager=manager_address,
    reserve=manager_address,
    freeze=manager_address,
    clawback=manager_address,
    index=117040603
)

# signing tx
signedTx = tx.sign(manager_private_key)

# sending transaction
try:
    txid2 = algod_client.send_transaction(signedTx)
    txid = signedTx.transaction.get_txid()
    print("transaction hash / tx ID : ",txid, "and", txid2)
    wait_for_confirmation(algod_client, txid)

except Exception as err:
    print(err)   