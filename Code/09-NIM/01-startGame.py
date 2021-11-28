import sys
import base64

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationCreateTxn
from algosdk.future.transaction import OnComplete
from algosdk.future.transaction import StateSchema
from utilities import wait_for_confirmation, getClient

def startGame(dealerMnemFile,approvalFile,directory):

    print("Starting a new istance of the 'NIM on Algorand' game")

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(dealerMnemFile,'r')
    dealerMnem=f.read()
    f.close()
    dealerSK=mnemonic.to_private_key(dealerMnem)
    dealerAddr=account.address_from_private_key(dealerSK)
    print("Dealer address: ",dealerAddr)

    on_complete=OnComplete.NoOpOC.real

    # declare application state storage (immutable)
    local_ints=0
    local_bytes=0
    global_ints=3 ##turn, max, and heap
    global_bytes=0

    # define schema
    globalSchema=StateSchema(global_ints,global_bytes)
    localSchema=StateSchema(local_ints,local_bytes)

    clearProgramSource=b"""#pragma version 4 int 1 """
    clearProgramResponse=algodClient.compile(clearProgramSource.decode('utf-8'))
    clearProgram=base64.b64decode(clearProgramResponse['result'])
    
    f=open(approvalFile,'r')
    approvalProgramSource=f.read()
    f.close()
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])

    utxn=ApplicationCreateTxn(dealerAddr,params,on_complete, \
                                        approvalProgram,clearProgram, \
                                        globalSchema,localSchema)
    ##uncomment to save the unsigned transaction
    ##write_to_file([utxn],"create.utxn")

    stxn=utxn.sign(dealerSK)
    ##uncomment to save the signed transaction
    ##write_to_file([stxn],"create.stxn")

    txId=stxn.transaction.get_txid()
    ##print("Transaction id:  ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    appId=txResponse['application-index']
    print("The new istance of the 'NIM on Algorand' game has id:",appId)

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <dealer mnem> <node directory>")
        exit()

    dealerMnemFile=sys.argv[1]
    approvalFile='nim.teal'
    directory=sys.argv[2]

    startGame(dealerMnemFile,approvalFile,directory)
    
