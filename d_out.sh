#!/bin/bash
# Generating aleatory data
rel=( 10 30 43 60 80 )
mn=0
path=$(pwd)
while [ $mn -le 4 ]; do
	N=100
	while [ $N -le 1000 ]; do
		i=1
		M=$(($N*${rel[$mn]}/10))
		at=$N
		if [ $N -lt 1000 ]; then
			at="0$at"
		fi
		while [ $i -le 10 ]; do
			num=$i
			if [ $i -lt 10 ]; then
				num="0$num"
			fi
			if [ $i -lt 100 ]; then
				num="0$num"
			fi
			infile="data/max3sat_mn${rel[$mn]}/in/${at}at_${num}.wcnf"
			outfile="data/max3sat_mn${rel[$mn]}/out/${at}at_${num}.txt"
			if [ -f $outfile ]; then
				continue
			fi
			cd solvers/toysat/
			./toysat --timeout=1800 --maxsat "$path/$infile" > "$path/$outfile"
			cd $path
			i=$(($i+1))
		done
		N=$(($N+100))
	done
	mn=$(($mn+1))
done
