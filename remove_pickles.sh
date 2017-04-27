#!/bin/bash
pickles=`find data/games-corpus/ -name *.pickle`

if [ -z "$pickles" ]; then
    echo No pickles to delete
else
    echo Deleting pickles
    echo $pickles
    rm $pickles
fi