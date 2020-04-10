#!/bin/bash

#read -p "Begin process? [Enter]"
#clear
#
#echo "Parsing input file..."
#cat temp.txt
#
#echo
#read -p "File parsed. Run python? [Enter]"
#clear
#
#python test.py
#
#echo
#read -p "Python complete. Good day! [Enter]"
#clear

echo "input testing"
read -p "Enter the site you would like to dig: " query

clear
rm -f output.txt

echo "Digging the website url: $query"

for recordType in A AAAA; do
    dig $ recordType $query +noadditional +noquestion +nocomments +nocmd +nostats >> output.txt
#    dig $recordType $query | tail -n +14 > temp.txt
#    (( count = $(wc -l < temp.txt) - 6 ))
#    head -n $count temp.txt >> output.txt
#     >> output.txt
done
rm -f temp.txt

open output.txt
