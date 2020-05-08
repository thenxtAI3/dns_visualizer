#!/bin/bash

read -p 'Enter query: ' query

echo 'Running probe...'

dnsviz probe -d 3 -p $query > rec.json
dnsviz probe -d 3 -p -A -a '.' $query > aut.json

echo 'Probe complete.'

echo 'Running script...'

python recursive.py $query

python authoritative.py $query

echo 'Thanks for playing!'