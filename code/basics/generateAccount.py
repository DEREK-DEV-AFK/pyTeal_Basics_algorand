from algosdk import account, encoding, mnemonic

# generate account
private_key, address = account.generate_account()
print('Private key :', private_key)
print('public address : ',address)
Mnemonic = mnemonic.from_private_key(private_key)
print("mnemonic : ", Mnemonic)

# check if the address is valid
if encoding.is_valid_address(address):
    print('valid')
else:
    print('invalid')  