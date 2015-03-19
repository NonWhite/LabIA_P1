#!/bin/bash
# Generating aleatory data
rel=( 10 30 43 60 80 )
mn=0
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
			name="data/max3sat_mn${rel[$mn]}/in/${at}at_${num}.wcnf"
			python generator/generator.py $N $M 3 $name
			#echo "N=$N , M=$M , FILE=$name"
			i=$(($i+1))
		done
		echo "N=$N , M=$M"
		N=$(($N+100))
	done
	mn=$(($mn+1))
done
