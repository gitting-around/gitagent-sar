#!/usr/bin/env bash
timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial3/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial3/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim1_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial3/ \;

./plot.py sim1_0.2 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_1_0.2_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_2_0.2_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_3_0.2_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_4_0.2_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_5_0.2_1.0
./plot.py sim1_0.5 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_1_0.5_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_2_0.5_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_3_0.5_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_4_0.5_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_5_0.5_1.0
./plot.py sim1_0.7 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_1_0.7_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_2_0.7_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_3_0.7_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_4_0.7_1.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim1/trial1/results_5_0.7_1.0

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.2.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial3/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.5.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial3/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch5_sim2_0.7.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial3/ \;

./plot.py sim2_0.2 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_1_0.2_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_2_0.2_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_3_0.2_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_4_0.2_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_5_0.2_2.0
./plot.py sim2_0.5 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_1_0.5_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_2_0.5_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_3_0.5_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_4_0.5_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_5_0.5_2.0
./plot.py sim2_0.7 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_1_0.7_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_2_0.7_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_3_0.7_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_4_0.7_2.0 ~/catkin_ws/results/test/pop_size.2/prova.2/sim2/trial1/results_5_0.7_2.0

find . -name 'sim*' | zip all.zip -@
./send.sh
