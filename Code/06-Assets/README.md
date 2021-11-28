# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Algorand Standard Assets (ASA) ##

### Step by step  ###

1. Run [createAsset.py](./createAsset.py) to create asset with name ```NovemberAssetXX```.
    It takes three command line arguments: the directory of the node, 
    the filename containing the mnemonic of the creator account, and
    the filename containing the address of the manager.
    Take note of the asset index that will be needed for the following steps.
2. [listCreatedAsset.py](./listCreatedAsset.py) can be used to list all assets created by an asset.
    It takes two command line arguments: 
    the directory of the node and 
    the filename containing the address of the creator for which we want to list the created assets.
    

3. Run [optinAsset.py](./optinAsset.py) to allow addresses to opt in the application.
    It takes three command line arguments: the directory of the node, 
    the filename containing the mnemonic of the address that wishes to opt in,  and 
    the asset index.

4. Run [transferAsset.py](./transferAsset.py) to transfer assets between two addresses. 
    It takes three command line arguments: the directory of the node, 
    the filename containing the mnemonic of the sender,
    the filename containing the address of the receiver,
    the asset index.
    
5. Run [destroyAsset.py](./destroyAsset.py) to destroy an asset.
    Note that it is required that all assets are owned by the manager.
    
