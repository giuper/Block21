#!/usr/bin/bash

##change this to the folder that contains goal
DIRECTORY=~/node
GOAL=${DIRECTORY}/goal

FILE=thirtyfour.teal
PASSWORD="34"

#uncomment next two lines if you want to run passphrase.teal
##FILE=passphrase.teal
##PASSWORD="weather comfort erupt verb pet range endorse exhibit tree brush crane man"

#address of receiver and closer
ADDR="IOYH24KGB6FMWWXDN3TUW35G6TUK45IQEOVKZKR6Z6MOLXURODKFCXX64Q"
OUTTX="out.stxn"

EncodedPass=$(echo -n ${PASSWORD} | base64 --wrap=0)
##echo ${EncodedPass}

${GOAL} clerk send -a 30000 --from-program ${FILE} -c ${ADDR} --argb64 ${EncodedPass} -t ${ADDR} -o ${OUTTX} -d ~/node/testnet


echo "Transaction found in file "${OUTTX}


