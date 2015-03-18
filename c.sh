echo "Eliminando archivos antiguos de entrada"
rm data/max2sat_100at/in/*
echo "Eliminando archivos antiguos de salida"
rm data/max2sat_100at/out/*
echo "Generando datos de entrada"
sh c_in.sh
echo "Ejecutando algoritmo y guardando datos de salida"
sh c_out.sh
