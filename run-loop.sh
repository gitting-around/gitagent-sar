#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $1 loop size, $2 name of script to loop"
  exit 1
fi
#script terminal_view_$1_$2
for i in $(seq 1 $1)
do
  mkdir /home/mfi01/catkin_ws/results/sandr/w\=25\,v\=5/trial$i
  mkdir /home/mfi01/catkin_ws/results/sandr/w\=50\,v\=10/trial$i
  mkdir /home/mfi01/catkin_ws/results/sandr/w\=75\,v\=15/trial$i
  mkdir /home/mfi01/catkin_ws/results/sandr/w\=100\,v\=20/trial$i

  echo "Running batch $i of simulations from script $2"
  ./$2 $i
  echo "Done batch $i of simulations, about to send results by email"
done
#exit
