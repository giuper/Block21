import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn
from algosdk.future.transaction import retrieve_from_file


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


def main():
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <Signed TX> <node directory>")
        exit()

    signedTXFile=sys.argv[1]
    directory=sys.argv[2]
    

    f=open(directory+"/algod.net",'r')
    algodAddr="http://"+f.read()[:-1]   #to remove the trailing newline
    f.close()
    f=open(directory+"/algod.token",'r')
    algodTok=f.read()
    f.close()
    algodClient = algod.AlgodClient(algodTok,algodAddr)

    txInL=retrieve_from_file(signedTXFile)
    for tx in txInL:
        txid=algodClient.send_transaction(tx)
        print(f'{"Signed transaction with txID:":32s}{txid:s}')
        print()
        try:
            confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
        except Exception as err:
            print(err)
            return

        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)))
        print("Decoded note: {}".format(base64.b64decode(
            confirmed_txn["txn"]["txn"]["note"]).decode()))

if __name__=='__main__':
    main()
