import sys
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationOptInTxn
from utilities import wait_for_confirmation, getClient


def signup(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(MnemFile,'r')
    Mnem=f.read()
    f.close()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    print("Address: ",Addr,"signing up for instance ",index,"of 'Nim on Algorand'")

    utxn=ApplicationOptInTxn(Addr,params,index)
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    signup(MnemFile,index,directory)
    
    
