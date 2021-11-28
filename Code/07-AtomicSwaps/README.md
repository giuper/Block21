# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Atomic Swaps ##

### Step by step  ###

Script [atomicSwap.py](./atomicSwap.py) takes as input two accounts ([Alice](./Accounts/Alice.addr) and 
[Bob](./Accounts/Bob.addr)), an asset id and the directory of the node.

It constructs two transactions:

1. Alice sends 10 Algos to Bob
2. Bob sends 5 instances of the asset to Alice

and either both are accepted or neither is.

We have the following transactions (use ```goal clerk inspect``` to see the content of the transactions)

1.  [Unsigned transaction from Alice to Bob](./TX/Alice2Bob.utnx)
2.  [Unsigned transaction from Alice to Bob with GID](./TX/Alice2BobwithGID.utnx)
3.  [Signed transaction from Alice to Bob with GID](./TX/Alice2BobwithGID.stnx)

and 
    
1.  [Unsigned transaction from Bob to Alice](./TX/Bob2Alice.utnx)
2.  [Unsigned transaction from Bob to Alice with GID](./TX/Bob2AlicewithGID.utnx)
3.  [Signed transaction from Bob to Alice with GID](./TX/Bob2AlicewithGID.stnx)

