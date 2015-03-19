#!/bin/bash
# Executing toysolver for data
path=$(pwd)
m=1
while [ $m -le 80 ]; do
#for m in {1..80}
#do
	i=1
	while [ $i -le 100 ]; do
	#for i in {1..100}
	#do
		x=$( echo "$((10*$m))")
		if [ $x -lt 100 ]; then
			x="0$x"
		fi
		num=$i
		if [ $i -lt 10 ]; then
			num="0$num"
		fi
		if [ $i -lt 100 ]; then
			num="0$num"
		fi
		infile="data/max2sat_100at/in/${x}cl_$num.wcnf"
		outfile="data/max2sat_100at/out/${x}cl_$num.txt"
		#./solvers/toysolver/toysolver/toysolver --maxsat $infile > $outfile
		cd solvers/toysat/
		./toysat --timeout=60 --maxsat "$path/$infile" > "$path/$outfile"
		cd $path
		i=$(($i+1))
	done
	m=$(($m+1))
done
