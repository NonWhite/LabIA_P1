#!/bin/bash
echo "Eliminando archivos antiguos de entrada"
rm data/max3sat_100at/in/*
echo "Eliminando archivos antiguos de salida"
rm data/max3sat_100at/out/*
echo "Generando datos de entrada"
sh b_in.sh
echo "Ejecutando algoritmo y guardando datos de salida"
sh b_out.sh
