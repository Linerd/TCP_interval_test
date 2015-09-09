#!/bin/bash
for((i=1;i<=$1;i++))
do
	sudo mn -c
	sudo python test.py -c $i
	sudo mn -c
	sudo python test.py -c $i -d $2
	sudo mn -c
	sudo python test.py -c $i -l $3
done
