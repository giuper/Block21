#!/usr/bin/bash

##change this to the folder that contains goal
DIRECTORY=~/node
GOAL=${DIRECTORY}/goal

OUTTX="out.stxn"

${GOAL} clerk rawsend -f ${OUTTX} -d ${DIRECTORY}/testnet




