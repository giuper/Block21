# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Code for smart (stateful) contracts  ##

We create a simple smart contract that exemplifies the use of global and local state.
Specifically, the contract maintains one global counter ```gcnt1``` (incremented by 1 at each invocation)
and one local counter ```lcnt``` (incremented by 7 at each invocation) per address.

### Step by step (no arguments) ###

1. Create the approval file [01-class.teal](01-class.teal)
2. Run [createApp.py](createApp.py) to create the application.
    It takes three command line arguments: the filename containing the mnemonic of the creator account,
        the filename containing the teal program, and the directory of the node.
    Take note of the application index that will be needed for the following steps.

    Note that you must use the creator address in the approval program. Currently the teal file  has the address
    that I have used during my lecture.

    [Here](./TX/create.stxn) is the signed transaction that creates an application.
    Use command ```goal clerk inspect create.stxn``` to view its content.

2. Run [optinApp.py](optinApp.py) to allow addresses to opt in the application.
    It takes three command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, and the directory of the node.

    [Here](./TX/optin.stxn) is the signed transaction to opt in an application.
    Use command ```goal clerk inspect optin.stxn``` to view its content.
    
3. Run [callApp.py](callApp.py) to allow addresses to execute the application.
    It takes three command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, and the directory of the node.
    
    [Here](./TX/noop.stxn) is the signed transaction to invoke an application.
    Use command ```goal clerk inspect noop.stxn``` to view its content.

    The output shows the current values of the counters.
    The global and local counter can be obtained from the ```response``` returned by the transaction once it 
    has completed (in the fields ```global-state-delta``` and ```local-state-delta```, respectively).
    Note that only variables whose values have changed are reported (whence the ```delta```).

    Alternatively, the local state can be obtained from the field ```apps-local-state``` of the 
    ```account_info``` obtained from the node about the address that has called the application.

    The global state can also be obtained from the script ```readGlobalValues.py``` that accesses 
    the ```account_info``` of the creator of the application.

### Step by step (with arguments) ###

1.  We modify the teal program so that the local value is incremented by a user provided 
integer (and not by 1 as before). [Here](02-class.teal) is the revised source.

2. Opting is the same as before.

3. Run [callIntArgApp.py](callIntArgApp.py) to allow addresses to execute the application
    and pass the parameter.

    It takes four command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, the increment and the directory of the node.
    

### Deleting the application ###

1. Run [deleteApp.py](deleteApp.py) to delete the contract
