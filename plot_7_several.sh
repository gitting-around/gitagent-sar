#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $1 nr of dirs to traverse, $2 dir basename"
  exit 1
fi
for i in $(seq 1 $1)
do
  cd $2$i
  ../bar1.sh $i
  cd ..

done