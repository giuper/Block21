# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Code for multi signatures ##
1. All in one
    1. [createMultiAddr.py](./createMultiAddr.py) creates a multi signature address
    2. [multiPayTXComplete.py](./multiPayTXComplete.py) creates, signs and submits a transaction from a multi signature address. The signature is 2 out of 3 and the P1, P2, P3 addresses in folder [Accounts](./Accounts) can be used to create the address and sign the transaction. The address in Accounts/receiver.addr can be used as a recipient of the transaction. The intermediate transactions are stored for inspection in folder TX.
    3. the whole process is executed by [example.sh](./example.sh)

2. Step by step: the script above assume that all signing keys are available to the script. This is not will happen in practice. Rather, the following process is executed
    1. The multi signature address is created by executing [createMultiAddr.py](./createMultiAddr.py)
    2. The unsigned transaction is created by executing [signMultiPayTX.py](./signMultiPayTX.py). That is, the first party to sign takes the unsigned transaction and adds its signature producing a transaction with one signature. Then the second party adds its signature to the transaction produced by the first party. This until we have the sufficient number of signatures (in the example, 2 signatures are sufficient).
    3. The fully-signed transaction is submitted to the blockchain.
    
