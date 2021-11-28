import sys
from algosdk import account
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn
from algosdk.future.transaction import write_to_file


def main():
    if len(sys.argv)!=6:
        print("usage: python3 "+sys.argv[0]+" <Addr1> <Addr2> <Addr3> <AddrRec> <node directory>")
        exit()

    amount=1_000_000
    version=1
    threshold=2

    receiverFile=sys.argv[4]
    directory=sys.argv[5]
    
    accounts=[]
    for filename in sys.argv[1:4]:
        f=open(filename+".addr",'r')
        acc=f.read()
        accounts.append(acc)
        f.close()
    mSig=Multisig(version,threshold,accounts)
    print(f'{"Multisig Address: ":22s}{mSig.address():s}')

    f=open(receiverFile+".addr",'r')
    receiver=f.read()
    f.close()
    
    f=open(directory+"/algod.net",'r')
    algodAddr="http://"+f.read()[:-1]
    f.close()
    f=open(directory+"/algod.token",'r')
    algodTok=f.read()
    f.close()
    algodClient = algod.AlgodClient(algodTok,algodAddr)

    account_info = algodClient.account_info(mSig.address())
    balance=account_info.get('amount')
    print(f'{"Account balance:":22s}{balance:d}{" microAlgos"}')
    if balance<amount:
        print("Insufficient funds")
        exit()

    params=algodClient.suggested_params()
    note="Ciao MultiPino!!!".encode()

    sAddr=mSig.address()
    unsignedTx=PaymentTxn(sAddr,params,receiver,amount,None,note)
    mTx=MultisigTransaction(unsignedTx,mSig)
    write_to_file([mTx],"TX/MultiPayWithPK.utx")
    print("Unsigned signature in TX/MultiPayWithPK.utx")


if __name__=='__main__':
    main()
