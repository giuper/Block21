import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from algosdk.future.transaction import AssetConfigTxn
from utilities import wait_for_confirmation, getClient

def create(directory,creatorMNEMFile,managerADDRFile):
    
    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    f=open(creatorMNEMFile,'r')
    creatorMnemo=f.read()
    f.close()
    creatorSK=mnemonic.to_private_key(creatorMnemo)
    creatorAddr=mnemonic.to_public_key(creatorMnemo)
    
    f=open(managerADDRFile,'r')
    managerAddr=f.read()
    f.close()
    reserveAddr=managerAddr
    freezeAddr=managerAddr
    clawbackAddr=managerAddr
    
    print("Creator Addr: ",creatorAddr)
    print("Manager Addr: ",managerAddr)
    print("Reserve Addr: ",reserveAddr)
    print("Freeze  Addr: ",freezeAddr) 
    print("ClawbackAddr: ",clawbackAddr)


    
    txn=AssetConfigTxn(
        sender=creatorAddr,
        sp=params,
        total=1000,
        default_frozen=False,
        unit_name="NvmberXX",
        asset_name="NovemberAssetXX",
        manager=managerAddr,
        reserve=reserveAddr,
        freeze=freezeAddr,
        clawback=clawbackAddr,
        url="https://giuper.github.io",
        decimals=0)

    transaction.write_to_file([txn],"assetCreation.utxn")

    # Sign with secret key of creator
    stxn=txn.sign(creatorSK)
    transaction.write_to_file([stxn],"assetCreation.stxn")

    # Send the transaction to the network and retrieve the txid.
    txid=algodClient.send_transaction(stxn)
    print("TX id:        ",txid)
    
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algodClient,txid,4)
    try:
        ptx=algodClient.pending_transaction_info(txid)
        assetId=ptx["asset-index"]
        print("Created an asset with id: ",assetId)
    except Exception as e:
        print(e)

    exit()


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python3 "+sys.argv[0]+" <NodeDir> <creator MNEM file> <manager ADDR>")
        exit()

    directory=sys.argv[1]
    creatorMNEMFile=sys.argv[2]
    managerADDRFile=sys.argv[3]

    create(directory,creatorMNEMFile,managerADDRFile)

