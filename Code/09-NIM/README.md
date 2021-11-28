# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Nim on Algorand ##

This simple smart contract implements a simple game of Nim between Alice and Bob.
Alice and Bob take turns in removing pebbles from a heap. 
The first player that cannot remove pebbles because none is left loses the game.
At each move there is a maximum number of pebbles that can be removed.

To play this game, three accounts are needed:
the Dealer's account, Alice's account and Bob's account

### Step by step  ###

1. Create the approval file by executing the [script](./createNim.sh) on input the [template](nim.tmpl).
    The script requires five arguments:
    1. The Dealer's address
    2. Alice's address
    3. Bob's address
    4. The initial number of pebbles
    5. The maximum number of pebbles a player can remove at each turn.
and produces the teal file ```nim.teal``` that will be the approval program for the smart contract.

    The file [nim.teal](nim.teal) is the teal file for 
    
    1.  dealer with address
        ```IUF3CPTWUN6NGASKHYJR7PCUUDKCDQCKGPMB577XYQ4CJRUZV3FDXEYL7Q```
    2. Alice with address
        ```ROM5Z3ESKA3PX3YGHKEH3RSASSR4PKKBSTQFMGPKU4NOESI6UVPMS77TTY```
    3. Bob with address
        ```5EKIODPFSULLMQT4K4KMVAECRKSWXN2QL7BB7IG4OQLHE4DS6QMEXEQ4LY```
    4. Initial number of pebbles ```12```
    5. Maximum number of pebbles removed in one move ```4```

2. The Dealer creates an instance of the game by running [01-startGame.py](01-startGame.py).
    The script requires the file containing the mnemonic of the dealer and the node directory.

3. The dealer [createApp.py](createApp.py) to create the application.
    It takes three command line arguments: the filename containing the mnemonic of the creator account,
        the filename containing the teal program, the directory of the node.
    Take note of the application index that will be needed by the players for the following steps.

4. The dealer signs up by running 
    [02-signupForGame.py](02-signupForGame.py). The script requires
    the filename containing the mnemonic of the player, the application index, and the node directory.

5. Alice and Bob sign up for the instance created by dealer by running
    [02-signupForGame.py](02-signupForGame.py). The script requires
    the filename containing the mnemonic of the player, the application index, and the node directory.

6. Players take turn in making moves, with Alice going first, by running 
  [03-makeMove.py](03-makeMove.py) that takes as arguments 
    the name of the file containing the mnemonic of the player, the instance index, the move, and
    the node directory.

7. At any time [readStatus.py](readStatus.py) can be used to read the current status of the game:
    the next player and the number pebbles left in the heap.

8. The instance of the game can be deleted by running [04-endGame.py](04-endGame.py)
