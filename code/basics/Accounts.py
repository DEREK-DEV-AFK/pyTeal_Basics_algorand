from algosdk import mnemonic

def fromPrivateKeyToMnemonic(pvtKey):
    return mnemonic.from_private_key(pvtKey)

private_key = 'BYd52rLWbunee8UdIXNPA9eN5KjDbcOba0+T/1bHo4OuarLKGXgXW7fUdF/VsI3yqQ9chv7wz1AizqNMv43vzA=='
result = fromPrivateKeyToMnemonic(private_key)
print('mnemonic for', private_key,' is : ')
print(result)
