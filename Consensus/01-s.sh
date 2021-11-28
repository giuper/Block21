#!/bin/bash

FIRST=$1
LAST=$2
ALGOK=~/node/algokey
GOAL=~/node/goal
ADDRESS=`cat consensus.addr`
DIRECTORY=~/node/testnet
PASSPhrase=`cat consensus.mnem`

echo "Step 1"
${GOAL} account addpartkey -a ${ADDRESS} --roundFirstValid=${FIRST} --roundLastValid=${LAST} --keyDilution=32 -d ${DIRECTORY}

echo "Step 2"
#${GOAL} account listpartkeys -d ${DIRECTORY} | grep ${ADDRESS} 

echo "Step 3"
#${GOAL} account partkeyinfo -d ${DIRECTORY} 

echo "Step 4"
${GOAL} account changeonlinestatus --address=${ADDRESS} --fee=2000 --firstvalid=${FIRST} --lastvalid=${LAST} --online=true --txfile=online.txn -d ${DIRECTORY}

##do not execute this on an online machine
##unless you are on the testnet
echo "Step 5" 
${ALGOK} sign -m ${PASSPhrase} -t online.txn -o algokeySigned.stxn

echo "Step 6"
${GOAL} clerk rawsend --filename algokeySigned.stxn -d ${DIRECTORY}
