#!/bin/bash


echo "the script is for circle run pso_all.py 10 time "



count=10

for((i=0;i<$count;))
do
 clear;
 echo "please waiting...,It's {$i} time" 
 python pso_all.py ./csvdata/compare_data.csv RMSE $1>>$1_result
 i=` expr $i+1 `
done
