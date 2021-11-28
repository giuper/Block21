import sys
import base64

from algosdk.future import transaction
from algosdk import mnemonic
from algosdk.v2client import algod
from pyteal import *


# utility function for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


if len(sys.argv)!=4:
    print("Usage: ",sys.argv[0],"<nodeDir> <receiver ADDR file> <TEAL program file>")
    exit()

nodeDir=sys.argv[1]
receiverADDRFile=sys.argv[2]
myprogram=sys.argv[3]

f=open(nodeDir+"/algod.net",'r')
algodAddr="http://"+f.read()[:-1]   #to remove the trailing newline
f.close()

f=open(nodeDir+"/algod.token",'r')
algodTok=f.read()
f.close()

algodClient=algod.AlgodClient(algodTok,algodAddr)

# Read TEAL program
data = open(myprogram, 'r').read()

# Compile TEAL program
response=algodClient.compile(data)
sender=response['hash']
programstr=response['result']
print("Response Result = ",programstr)
print("Response Hash   = ",sender)

# Create logic sig
t = programstr.encode()
program = base64.decodebytes(t)

# Create arg to pass if TEAL program requires an arg,
# if not, omit args param
# string parameter

arg_str = "34"
arg1=arg_str.encode()
lsig=transaction.LogicSig(program, args=[arg1])

receiver=open(receiverADDRFile,'r').read()[:-1] 
closeremainderto=receiver
params=algodClient.suggested_params()
txn = transaction.PaymentTxn(
        sender, params, receiver, 30000, closeremainderto)

# Create the LogicSigTransaction with contract account LogicSig
lstx=transaction.LogicSigTransaction(txn,lsig)
transaction.write_to_file([lstx],"simple.stxn")
# Send raw LogicSigTransaction to network
try:
    txid = algodClient.send_transaction(lstx)
    print("Transaction ID  = " + txid)
except Exception as e:
    print(e)
    exit()

wait_for_confirmation(algodClient, txid,4)
