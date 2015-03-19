#!/bin/bash
rel=( 10 30 43 60 80 )
mn=0
echo "Eliminando archivos antiguos de entrada"
while [ $mn -le 4 ]; do
	dir="data/max3sat_mn${rel[$mn]}/in/"
	rm -r $dir
	mkdir $dir
	mn=$(($mn+1))
done

mn=0
echo "Eliminando archivos antiguos de salida"
while [ $mn -le 4 ]; do
	dir="data/max3sat_mn${rel[$mn]}/out/"
	rm -r $dir
	mkdir $dir
	mn=$(($mn+1))
done

echo "Generando datos de entrada"
./d_in.sh
echo "Ejecutando algoritmo y guardando datos de salida"
./d_out.sh
