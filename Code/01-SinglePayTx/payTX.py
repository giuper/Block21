import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn, write_to_file


def payTX(sKey,sAddr,rAddr,amount,algodClient):

    params = algodClient.suggested_params()

    note="Ciao Pino!!!".encode()

    unsignedTx=PaymentTxn(sAddr,params,rAddr,amount,None,note)
    write_to_file([unsignedTx],"TX/Pay.utx")

    signedTx=unsignedTx.sign(sKey)
    write_to_file([signedTx],"TX/Pay.stx")

    txid=algodClient.send_transaction(signedTx)
    print(f'{"Signed transaction with txID:":32s}{txid:s}')
    print()

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    account_info = algodClient.account_info(sAddr)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

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
    if len(sys.argv)!=4:
        print("usage: "+sys.argv[0]+" <file with sender key> <file with receiver addr> <node directory>")
        exit()

    destPublicArg=2
    amount=1_000_000

    directory=sys.argv[3]
    f=open(directory+"/algod.token",'r')
    algodToken=f.read()
    f.close()
    f=open(directory+"/algod.net",'r')
    algodAddress="http://"+f.read()[:-1]   #to remove the trailing newline
    f.close()
    algodClient = algod.AlgodClient(algodToken,algodAddress)

    senderKeyF=sys.argv[1]
    f=open(senderKeyF,'r')
    passphrase=f.read()
    f.close()
    sKey=mnemonic.to_private_key(passphrase)
    sAddr=mnemonic.to_public_key(passphrase)
    print(f'{"Sender address:":32s}{sAddr:s}')

    account_info = algodClient.account_info(sAddr)
    balance=account_info.get('amount')
    print(f'{"Account balance:":32s}{balance:d}{" microAlgos"}')

    receiverAddrF=sys.argv[2]
    f=open(receiverAddrF,'r')
    rAddr=f.read()
    f.close()
    print(f'{"Receiver address:":32s}{rAddr:s}')

    if (amount<=balance):
        payTX(sKey,sAddr,rAddr,amount,algodClient)
    else:
        print("Insufficient funds")

if __name__=='__main__':
    main()
