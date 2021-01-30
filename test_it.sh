#!/bin/bash

# Lokalno generisane instance
for method in "f" "b" "m"
do
    for cur in 0 4
    do
	for var in 0 1 2 3
	do
	    python3 main.py -$method\s `expr $var + $cur` &
	done
	wait
    done
    wait
done

# kexu instance
for method in "b" "m"
do
    for cur in 0 5
    do
	for var in 0 1 2 3 4
	do
	    python3 main.py -$method\k `expr $var + $cur` &
	done
	wait
    done
    wait
done

# delorme instance
for method in "b" "m"
do
    for cur in 0 4 8 12 16 20 24 28 32 36 40 44 48 52
    do
	for var in 0 1 2 3
	do
	    python3 main.py -$method\d `expr $var + $cur` &
	done
	wait
    done
    wait
done


