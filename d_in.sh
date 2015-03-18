# Generating aleatory data
mn=1
rel=(10 30 43 60 80)
while [ $mn -le 5 ]; do
	N=100
	while [ $N -le 1000 ]; do
		i=1
		while [ $i -le 100 ]; do
			M=$(($N*${rel[$mn]}/10))
			echo $M
			i=$(($i+1))
		done
		n=$(($n+100))
	done
	#
	#while [ $i -le 100 ]; do
	#	x=$( echo "$((10*$m))")
	#	if [ $x -lt 100 ]; then
	#		x="0$x"
	#	fi
	#	num=$i
	#	if [ $i -lt 10 ]; then
	#		num="0$num"
	#	fi
	#	if [ $i -lt 100 ]; then
	#		num="0$num"
	#	fi
	#	name="data/max3sat_100at/in/${x}cl_$num.wcnf"
	#	python generator/generator.py 100 $x 3 $name
	#	i=$(($i+1))
	#done
	#m=$(($m+1))
done
