# Blockchain21: *Blockchain* #
### Academic year 2021/22 ###

## Smart signatures from the Command Line ##
    
We have two simple teal programs:

1. [thirtyfour.teal](./thirtyfour.teal) that is happy when run with one argument equal to "34" and the sender of the transaction will get the whole balance when the account is closed.


2. [passphrase.teal](./passphrase.teal) that is happy when run with one argument whose SHA256 hash is equal to the value 30AT2gOReDBdJmLBO/DgvjC6hIXgACecTpFDcP1bJHU= (encoded in base64)

Both can be used as a basis for a smart signature, following these three steps:

1. [Compile the teal program](./00compile.sh)
The compilation process will output the address of the smart signature and the compiled program
(see the .tok file). Use the dispenser of the testnet to fund the account.

2. [Create the transaction](./01createTX.sh)
The smartly signed transaction is output in file out.stxn.

3. [Submit the transaction](./02send.sh)
The transaction in file out.stxn is send to the client

