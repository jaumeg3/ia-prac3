#!/usr/bin/env bash

vector=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
for x in $(ls -d test/*".data"); do
    for i in ${vector[@]}; do
        #for j in $(seq 1 1 10); do
        echo $i $(python src/treepredict.py -ifl $x -p $i) >> $x.log.txt
        #done
    done
done