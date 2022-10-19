from algosdk.v2client import algod
from algosdk import mnemonic, account
from algosdk import transaction

def make_algod_client(apiLink, apiKey):
    algo_api_link = apiLink
    algo_key = apiKey
    headers = {
        "X-API-Key": algo_key
    }

    algo_client = algod.AlgodClient(algo_api_link,algo_key,headers)
    return algo_client