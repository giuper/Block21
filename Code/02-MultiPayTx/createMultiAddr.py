import sys
from algosdk import mnemonic
from algosdk.future.transaction import Multisig

if len(sys.argv)!=4:
    print("usage: "+sys.argv[0]+" <file P1 addr> <file P2 addr> <file P3 addr>")
    exit()

accounts=[]
for i in range(3):
    f=open(sys.argv[i+1]+".addr",'r')
    account=f.read()
    accounts.append(account)
    f.close()
print("Accounts:")
print(accounts)

# create a multisig account
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
msig = Multisig(version, threshold, accounts)
print("Multisig Address: ", msig.address())
print("Please go to: https://bank.testnet.algorand.network/ to fund multisig account.")
