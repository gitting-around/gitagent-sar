#!/usr/bin/env bash
chmod a+x /home/mfi01/catkin_ws/src/gitagent/result_scripts/plot_3.py /home/mfi01/catkin_ws/src/gitagent/result_scripts/heatmap.py chmod a+x /home/mfi01/catkin_ws/src/gitagent/result_scripts/plot_3.py /home/mfi01/catkin_ws/src/gitagent/result_scripts/send.sh

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05 \;

cd ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.05/

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.05_\[0\,\ 0\] results_2_0.0_0.0_0.05_\[0\,\ 0\] results_3_0.0_0.0_0.05_\[0\,\ 0\] results_4_0.0_0.0_0.05_\[0\,\ 0\] results_5_0.0_0.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.05_\[0\,\ 0\] results_2_0.5_0.0_0.05_\[0\,\ 0\] results_3_0.5_0.0_0.05_\[0\,\ 0\] results_4_0.5_0.0_0.05_\[0\,\ 0\] results_5_0.5_0.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.05_\[0\,\ 0\] results_2_1.0_0.0_0.05_\[0\,\ 0\] results_3_1.0_0.0_0.05_\[0\,\ 0\] results_4_1.0_0.0_0.05_\[0\,\ 0\] results_5_1.0_0.0_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.05_\[0\,\ 0\] results_2_0.0_0.5_0.05_\[0\,\ 0\] results_3_0.0_0.5_0.05_\[0\,\ 0\] results_4_0.0_0.5_0.05_\[0\,\ 0\] results_5_0.0_0.5_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.05_\[0\,\ 0\] results_2_0.5_0.5_0.05_\[0\,\ 0\] results_3_0.5_0.5_0.05_\[0\,\ 0\] results_4_0.5_0.5_0.05_\[0\,\ 0\] results_5_0.5_0.5_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.05_\[0\,\ 0\] results_2_1.0_0.5_0.05_\[0\,\ 0\] results_3_1.0_0.5_0.05_\[0\,\ 0\] results_4_1.0_0.5_0.05_\[0\,\ 0\] results_5_1.0_0.5_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.05_\[0\,\ 0\] results_2_0.0_1.0_0.05_\[0\,\ 0\] results_3_0.0_1.0_0.05_\[0\,\ 0\] results_4_0.0_1.0_0.05_\[0\,\ 0\] results_5_0.0_1.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.05_\[0\,\ 0\] results_2_0.5_1.0_0.05_\[0\,\ 0\] results_3_0.5_1.0_0.05_\[0\,\ 0\] results_4_0.5_1.0_0.05_\[0\,\ 0\] results_5_0.5_1.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.05_\[0\,\ 0\] results_2_1.0_1.0_0.05_\[0\,\ 0\] results_3_1.0_1.0_0.05_\[0\,\ 0\] results_4_1.0_1.0_0.05_\[0\,\ 0\] results_5_1.0_1.0_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_nomem_0_05.jpg
mv dynamicdepend_heatmap.jpg depend_nomem_0_05.jpg

find . -name '*.jpg' | zip dynamic_nomem_0.05.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_nomem_0.05.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125 \;

cd ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.125_\[0\,\ 0\] results_2_0.0_0.0_0.125_\[0\,\ 0\] results_3_0.0_0.0_0.125_\[0\,\ 0\] results_4_0.0_0.0_0.125_\[0\,\ 0\] results_5_0.0_0.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.125_\[0\,\ 0\] results_2_0.5_0.0_0.125_\[0\,\ 0\] results_3_0.5_0.0_0.125_\[0\,\ 0\] results_4_0.5_0.0_0.125_\[0\,\ 0\] results_5_0.5_0.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.125_\[0\,\ 0\] results_2_1.0_0.0_0.125_\[0\,\ 0\] results_3_1.0_0.0_0.125_\[0\,\ 0\] results_4_1.0_0.0_0.125_\[0\,\ 0\] results_5_1.0_0.0_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.125_\[0\,\ 0\] results_2_0.0_0.5_0.125_\[0\,\ 0\] results_3_0.0_0.5_0.125_\[0\,\ 0\] results_4_0.0_0.5_0.125_\[0\,\ 0\] results_5_0.0_0.5_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.125_\[0\,\ 0\] results_2_0.5_0.5_0.125_\[0\,\ 0\] results_3_0.5_0.5_0.125_\[0\,\ 0\] results_4_0.5_0.5_0.125_\[0\,\ 0\] results_5_0.5_0.5_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.125_\[0\,\ 0\] results_2_1.0_0.5_0.125_\[0\,\ 0\] results_3_1.0_0.5_0.125_\[0\,\ 0\] results_4_1.0_0.5_0.125_\[0\,\ 0\] results_5_1.0_0.5_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.125_\[0\,\ 0\] results_2_0.0_1.0_0.125_\[0\,\ 0\] results_3_0.0_1.0_0.125_\[0\,\ 0\] results_4_0.0_1.0_0.125_\[0\,\ 0\] results_5_0.0_1.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.125_\[0\,\ 0\] results_2_0.5_1.0_0.125_\[0\,\ 0\] results_3_0.5_1.0_0.125_\[0\,\ 0\] results_4_0.5_1.0_0.125_\[0\,\ 0\] results_5_0.5_1.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.125_\[0\,\ 0\] results_2_1.0_1.0_0.125_\[0\,\ 0\] results_3_1.0_1.0_0.125_\[0\,\ 0\] results_4_1.0_1.0_0.125_\[0\,\ 0\] results_5_1.0_1.0_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_nomem_0_125.jpg
mv dynamicdepend_heatmap.jpg depend_nomem_0_125.jpg

find . -name '*.jpg' | zip dynamic_nomem_0.125.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_nomem_0.125.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2 \;


cd ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.2_\[0\,\ 0\] results_2_0.0_0.0_0.2_\[0\,\ 0\] results_3_0.0_0.0_0.2_\[0\,\ 0\] results_4_0.0_0.0_0.2_\[0\,\ 0\] results_5_0.0_0.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.2_\[0\,\ 0\] results_2_0.5_0.0_0.2_\[0\,\ 0\] results_3_0.5_0.0_0.2_\[0\,\ 0\] results_4_0.5_0.0_0.2_\[0\,\ 0\] results_5_0.5_0.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.2_\[0\,\ 0\] results_2_1.0_0.0_0.2_\[0\,\ 0\] results_3_1.0_0.0_0.2_\[0\,\ 0\] results_4_1.0_0.0_0.2_\[0\,\ 0\] results_5_1.0_0.0_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.2_\[0\,\ 0\] results_2_0.0_0.5_0.2_\[0\,\ 0\] results_3_0.0_0.5_0.2_\[0\,\ 0\] results_4_0.0_0.5_0.2_\[0\,\ 0\] results_5_0.0_0.5_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.2_\[0\,\ 0\] results_2_0.5_0.5_0.2_\[0\,\ 0\] results_3_0.5_0.5_0.2_\[0\,\ 0\] results_4_0.5_0.5_0.2_\[0\,\ 0\] results_5_0.5_0.5_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.2_\[0\,\ 0\] results_2_1.0_0.5_0.2_\[0\,\ 0\] results_3_1.0_0.5_0.2_\[0\,\ 0\] results_4_1.0_0.5_0.2_\[0\,\ 0\] results_5_1.0_0.5_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.2_\[0\,\ 0\] results_2_0.0_1.0_0.2_\[0\,\ 0\] results_3_0.0_1.0_0.2_\[0\,\ 0\] results_4_0.0_1.0_0.2_\[0\,\ 0\] results_5_0.0_1.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.2_\[0\,\ 0\] results_2_0.5_1.0_0.2_\[0\,\ 0\] results_3_0.5_1.0_0.2_\[0\,\ 0\] results_4_0.5_1.0_0.2_\[0\,\ 0\] results_5_0.5_1.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.2_\[0\,\ 0\] results_2_1.0_1.0_0.2_\[0\,\ 0\] results_3_1.0_1.0_0.2_\[0\,\ 0\] results_4_1.0_1.0_0.2_\[0\,\ 0\] results_5_1.0_1.0_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_nomem_0_2.jpg
mv dynamicdepend_heatmap.jpg depend_nomem_0_2.jpg

find . -name '*.jpg' | zip dynamic_nomem_0.2.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_nomem_0.2.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.05 \;                                                                                                                  

cd ~/catkin_ws/results/braitenberg_1/static/pressure_0.05/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.0' results_1_0.0_0.0_0.05_\[1\,\ 1\] results_2_0.0_0.0_0.05_\[1\,\ 1\] results_3_0.0_0.0_0.05_\[1\,\ 1\] results_4_0.0_0.0_0.05_\[1\,\ 1\] results_5_0.0_0.0_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.0' results_1_0.5_0.0_0.05_\[1\,\ 1\] results_2_0.5_0.0_0.05_\[1\,\ 1\] results_3_0.5_0.0_0.05_\[1\,\ 1\] results_4_0.5_0.0_0.05_\[1\,\ 1\] results_5_0.5_0.0_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.0' results_1_1.0_0.0_0.05_\[1\,\ 1\] results_2_1.0_0.0_0.05_\[1\,\ 1\] results_3_1.0_0.0_0.05_\[1\,\ 1\] results_4_1.0_0.0_0.05_\[1\,\ 1\] results_5_1.0_0.0_0.05_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.5' results_1_0.0_0.5_0.05_\[1\,\ 1\] results_2_0.0_0.5_0.05_\[1\,\ 1\] results_3_0.0_0.5_0.05_\[1\,\ 1\] results_4_0.0_0.5_0.05_\[1\,\ 1\] results_5_0.0_0.5_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.5' results_1_0.5_0.5_0.05_\[1\,\ 1\] results_2_0.5_0.5_0.05_\[1\,\ 1\] results_3_0.5_0.5_0.05_\[1\,\ 1\] results_4_0.5_0.5_0.05_\[1\,\ 1\] results_5_0.5_0.5_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.5' results_1_1.0_0.5_0.05_\[1\,\ 1\] results_2_1.0_0.5_0.05_\[1\,\ 1\] results_3_1.0_0.5_0.05_\[1\,\ 1\] results_4_1.0_0.5_0.05_\[1\,\ 1\] results_5_1.0_0.5_0.05_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_1.0' results_1_0.0_1.0_0.05_\[1\,\ 1\] results_2_0.0_1.0_0.05_\[1\,\ 1\] results_3_0.0_1.0_0.05_\[1\,\ 1\] results_4_0.0_1.0_0.05_\[1\,\ 1\] results_5_0.0_1.0_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_1.0' results_1_0.5_1.0_0.05_\[1\,\ 1\] results_2_0.5_1.0_0.05_\[1\,\ 1\] results_3_0.5_1.0_0.05_\[1\,\ 1\] results_4_0.5_1.0_0.05_\[1\,\ 1\] results_5_0.5_1.0_0.05_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_1.0' results_1_1.0_1.0_0.05_\[1\,\ 1\] results_2_1.0_1.0_0.05_\[1\,\ 1\] results_3_1.0_1.0_0.05_\[1\,\ 1\] results_4_1.0_1.0_0.05_\[1\,\ 1\] results_5_1.0_1.0_0.05_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py static static_total
mv dynamicall_heatmap.jpg all_static_0_05.jpg
mv dynamicdepend_heatmap.jpg depend_static_0_05.jpg

find . -name '*.jpg' | zip static_nomem_0.05.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh static_nomem_0.05.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125 \;

cd ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.0' results_1_0.0_0.0_0.125_\[1\,\ 1\] results_2_0.0_0.0_0.125_\[1\,\ 1\] results_3_0.0_0.0_0.125_\[1\,\ 1\] results_4_0.0_0.0_0.125_\[1\,\ 1\] results_5_0.0_0.0_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.0' results_1_0.5_0.0_0.125_\[1\,\ 1\] results_2_0.5_0.0_0.125_\[1\,\ 1\] results_3_0.5_0.0_0.125_\[1\,\ 1\] results_4_0.5_0.0_0.125_\[1\,\ 1\] results_5_0.5_0.0_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.0' results_1_1.0_0.0_0.125_\[1\,\ 1\] results_2_1.0_0.0_0.125_\[1\,\ 1\] results_3_1.0_0.0_0.125_\[1\,\ 1\] results_4_1.0_0.0_0.125_\[1\,\ 1\] results_5_1.0_0.0_0.125_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.5' results_1_0.0_0.5_0.125_\[1\,\ 1\] results_2_0.0_0.5_0.125_\[1\,\ 1\] results_3_0.0_0.5_0.125_\[1\,\ 1\] results_4_0.0_0.5_0.125_\[1\,\ 1\] results_5_0.0_0.5_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.5' results_1_0.5_0.5_0.125_\[1\,\ 1\] results_2_0.5_0.5_0.125_\[1\,\ 1\] results_3_0.5_0.5_0.125_\[1\,\ 1\] results_4_0.5_0.5_0.125_\[1\,\ 1\] results_5_0.5_0.5_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.5' results_1_1.0_0.5_0.125_\[1\,\ 1\] results_2_1.0_0.5_0.125_\[1\,\ 1\] results_3_1.0_0.5_0.125_\[1\,\ 1\] results_4_1.0_0.5_0.125_\[1\,\ 1\] results_5_1.0_0.5_0.125_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_1.0' results_1_0.0_1.0_0.125_\[1\,\ 1\] results_2_0.0_1.0_0.125_\[1\,\ 1\] results_3_0.0_1.0_0.125_\[1\,\ 1\] results_4_0.0_1.0_0.125_\[1\,\ 1\] results_5_0.0_1.0_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_1.0' results_1_0.5_1.0_0.125_\[1\,\ 1\] results_2_0.5_1.0_0.125_\[1\,\ 1\] results_3_0.5_1.0_0.125_\[1\,\ 1\] results_4_0.5_1.0_0.125_\[1\,\ 1\] results_5_0.5_1.0_0.125_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_1.0' results_1_1.0_1.0_0.125_\[1\,\ 1\] results_2_1.0_1.0_0.125_\[1\,\ 1\] results_3_1.0_1.0_0.125_\[1\,\ 1\] results_4_1.0_1.0_0.125_\[1\,\ 1\] results_5_1.0_1.0_0.125_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py static static_total
mv dynamicall_heatmap.jpg all_static_0_125.jpg
mv dynamicdepend_heatmap.jpg depend_static_0_125.jpg

find . -name '*.jpg' | zip static_nomem_0.125.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh static_nomem_0.125.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2 \;


cd ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.0' results_1_0.0_0.0_0.2_\[1\,\ 1\] results_2_0.0_0.0_0.2_\[1\,\ 1\] results_3_0.0_0.0_0.2_\[1\,\ 1\] results_4_0.0_0.0_0.2_\[1\,\ 1\] results_5_0.0_0.0_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.0' results_1_0.5_0.0_0.2_\[1\,\ 1\] results_2_0.5_0.0_0.2_\[1\,\ 1\] results_3_0.5_0.0_0.2_\[1\,\ 1\] results_4_0.5_0.0_0.2_\[1\,\ 1\] results_5_0.5_0.0_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.0' results_1_1.0_0.0_0.2_\[1\,\ 1\] results_2_1.0_0.0_0.2_\[1\,\ 1\] results_3_1.0_0.0_0.2_\[1\,\ 1\] results_4_1.0_0.0_0.2_\[1\,\ 1\] results_5_1.0_0.0_0.2_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_0.5' results_1_0.0_0.5_0.2_\[1\,\ 1\] results_2_0.0_0.5_0.2_\[1\,\ 1\] results_3_0.0_0.5_0.2_\[1\,\ 1\] results_4_0.0_0.5_0.2_\[1\,\ 1\] results_5_0.0_0.5_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_0.5' results_1_0.5_0.5_0.2_\[1\,\ 1\] results_2_0.5_0.5_0.2_\[1\,\ 1\] results_3_0.5_0.5_0.2_\[1\,\ 1\] results_4_0.5_0.5_0.2_\[1\,\ 1\] results_5_0.5_0.5_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_0.5' results_1_1.0_0.5_0.2_\[1\,\ 1\] results_2_1.0_0.5_0.2_\[1\,\ 1\] results_3_1.0_0.5_0.2_\[1\,\ 1\] results_4_1.0_0.5_0.2_\[1\,\ 1\] results_5_1.0_0.5_0.2_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.0_1.0' results_1_0.0_1.0_0.2_\[1\,\ 1\] results_2_0.0_1.0_0.2_\[1\,\ 1\] results_3_0.0_1.0_0.2_\[1\,\ 1\] results_4_0.0_1.0_0.2_\[1\,\ 1\] results_5_0.0_1.0_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '0.5_1.0' results_1_0.5_1.0_0.2_\[1\,\ 1\] results_2_0.5_1.0_0.2_\[1\,\ 1\] results_3_0.5_1.0_0.2_\[1\,\ 1\] results_4_0.5_1.0_0.2_\[1\,\ 1\] results_5_0.5_1.0_0.2_\[1\,\ 1\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py static '1.0_1.0' results_1_1.0_1.0_0.2_\[1\,\ 1\] results_2_1.0_1.0_0.2_\[1\,\ 1\] results_3_1.0_1.0_0.2_\[1\,\ 1\] results_4_1.0_1.0_0.2_\[1\,\ 1\] results_5_1.0_1.0_0.2_\[1\,\ 1\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py static static_total
mv dynamicall_heatmap.jpg all_static_0_2.jpg
mv dynamicdepend_heatmap.jpg depend_static_0_2.jpg

find . -name '*.jpg' | zip static_nomem_0.2.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh static_nomem_0.2.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05 \;

cd ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.05/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.05_\[0\,\ 0\] results_2_0.0_0.0_0.05_\[0\,\ 0\] results_3_0.0_0.0_0.05_\[0\,\ 0\] results_4_0.0_0.0_0.05_\[0\,\ 0\] results_5_0.0_0.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.05_\[0\,\ 0\] results_2_0.5_0.0_0.05_\[0\,\ 0\] results_3_0.5_0.0_0.05_\[0\,\ 0\] results_4_0.5_0.0_0.05_\[0\,\ 0\] results_5_0.5_0.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.05_\[0\,\ 0\] results_2_1.0_0.0_0.05_\[0\,\ 0\] results_3_1.0_0.0_0.05_\[0\,\ 0\] results_4_1.0_0.0_0.05_\[0\,\ 0\] results_5_1.0_0.0_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.05_\[0\,\ 0\] results_2_0.0_0.5_0.05_\[0\,\ 0\] results_3_0.0_0.5_0.05_\[0\,\ 0\] results_4_0.0_0.5_0.05_\[0\,\ 0\] results_5_0.0_0.5_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.05_\[0\,\ 0\] results_2_0.5_0.5_0.05_\[0\,\ 0\] results_3_0.5_0.5_0.05_\[0\,\ 0\] results_4_0.5_0.5_0.05_\[0\,\ 0\] results_5_0.5_0.5_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.05_\[0\,\ 0\] results_2_1.0_0.5_0.05_\[0\,\ 0\] results_3_1.0_0.5_0.05_\[0\,\ 0\] results_4_1.0_0.5_0.05_\[0\,\ 0\] results_5_1.0_0.5_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.05_\[0\,\ 0\] results_2_0.0_1.0_0.05_\[0\,\ 0\] results_3_0.0_1.0_0.05_\[0\,\ 0\] results_4_0.0_1.0_0.05_\[0\,\ 0\] results_5_0.0_1.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.05_\[0\,\ 0\] results_2_0.5_1.0_0.05_\[0\,\ 0\] results_3_0.5_1.0_0.05_\[0\,\ 0\] results_4_0.5_1.0_0.05_\[0\,\ 0\] results_5_0.5_1.0_0.05_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.05_\[0\,\ 0\] results_2_1.0_1.0_0.05_\[0\,\ 0\] results_3_1.0_1.0_0.05_\[0\,\ 0\] results_4_1.0_1.0_0.05_\[0\,\ 0\] results_5_1.0_1.0_0.05_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_mem_0_05.jpg
mv dynamicdepend_heatmap.jpg depend_mem_0_05.jpg

find . -name '*.jpg' | zip dynamic_mem_0.05.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_mem_0.05.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125 \;

cd ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/

chmod a+x plot_3.py heatmap.py

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.125_\[0\,\ 0\] results_2_0.0_0.0_0.125_\[0\,\ 0\] results_3_0.0_0.0_0.125_\[0\,\ 0\] results_4_0.0_0.0_0.125_\[0\,\ 0\] results_5_0.0_0.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.125_\[0\,\ 0\] results_2_0.5_0.0_0.125_\[0\,\ 0\] results_3_0.5_0.0_0.125_\[0\,\ 0\] results_4_0.5_0.0_0.125_\[0\,\ 0\] results_5_0.5_0.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.125_\[0\,\ 0\] results_2_1.0_0.0_0.125_\[0\,\ 0\] results_3_1.0_0.0_0.125_\[0\,\ 0\] results_4_1.0_0.0_0.125_\[0\,\ 0\] results_5_1.0_0.0_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.125_\[0\,\ 0\] results_2_0.0_0.5_0.125_\[0\,\ 0\] results_3_0.0_0.5_0.125_\[0\,\ 0\] results_4_0.0_0.5_0.125_\[0\,\ 0\] results_5_0.0_0.5_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.125_\[0\,\ 0\] results_2_0.5_0.5_0.125_\[0\,\ 0\] results_3_0.5_0.5_0.125_\[0\,\ 0\] results_4_0.5_0.5_0.125_\[0\,\ 0\] results_5_0.5_0.5_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.125_\[0\,\ 0\] results_2_1.0_0.5_0.125_\[0\,\ 0\] results_3_1.0_0.5_0.125_\[0\,\ 0\] results_4_1.0_0.5_0.125_\[0\,\ 0\] results_5_1.0_0.5_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.125_\[0\,\ 0\] results_2_0.0_1.0_0.125_\[0\,\ 0\] results_3_0.0_1.0_0.125_\[0\,\ 0\] results_4_0.0_1.0_0.125_\[0\,\ 0\] results_5_0.0_1.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.125_\[0\,\ 0\] results_2_0.5_1.0_0.125_\[0\,\ 0\] results_3_0.5_1.0_0.125_\[0\,\ 0\] results_4_0.5_1.0_0.125_\[0\,\ 0\] results_5_0.5_1.0_0.125_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.125_\[0\,\ 0\] results_2_1.0_1.0_0.125_\[0\,\ 0\] results_3_1.0_1.0_0.125_\[0\,\ 0\] results_4_1.0_1.0_0.125_\[0\,\ 0\] results_5_1.0_1.0_0.125_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_mem_0_125.jpg
mv dynamicdepend_heatmap.jpg depend_mem_0_125.jpg

find . -name '*.jpg' | zip dynamic_mem_0.125.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_mem_0.125.zip

cd ~/catkin_ws/

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

timeout 26m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2 \;

cd ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.0' results_1_0.0_0.0_0.2_\[0\,\ 0\] results_2_0.0_0.0_0.2_\[0\,\ 0\] results_3_0.0_0.0_0.2_\[0\,\ 0\] results_4_0.0_0.0_0.2_\[0\,\ 0\] results_5_0.0_0.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.0' results_1_0.5_0.0_0.2_\[0\,\ 0\] results_2_0.5_0.0_0.2_\[0\,\ 0\] results_3_0.5_0.0_0.2_\[0\,\ 0\] results_4_0.5_0.0_0.2_\[0\,\ 0\] results_5_0.5_0.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.0' results_1_1.0_0.0_0.2_\[0\,\ 0\] results_2_1.0_0.0_0.2_\[0\,\ 0\] results_3_1.0_0.0_0.2_\[0\,\ 0\] results_4_1.0_0.0_0.2_\[0\,\ 0\] results_5_1.0_0.0_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_0.5' results_1_0.0_0.5_0.2_\[0\,\ 0\] results_2_0.0_0.5_0.2_\[0\,\ 0\] results_3_0.0_0.5_0.2_\[0\,\ 0\] results_4_0.0_0.5_0.2_\[0\,\ 0\] results_5_0.0_0.5_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_0.5' results_1_0.5_0.5_0.2_\[0\,\ 0\] results_2_0.5_0.5_0.2_\[0\,\ 0\] results_3_0.5_0.5_0.2_\[0\,\ 0\] results_4_0.5_0.5_0.2_\[0\,\ 0\] results_5_0.5_0.5_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_0.5' results_1_1.0_0.5_0.2_\[0\,\ 0\] results_2_1.0_0.5_0.2_\[0\,\ 0\] results_3_1.0_0.5_0.2_\[0\,\ 0\] results_4_1.0_0.5_0.2_\[0\,\ 0\] results_5_1.0_0.5_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.0_1.0' results_1_0.0_1.0_0.2_\[0\,\ 0\] results_2_0.0_1.0_0.2_\[0\,\ 0\] results_3_0.0_1.0_0.2_\[0\,\ 0\] results_4_0.0_1.0_0.2_\[0\,\ 0\] results_5_0.0_1.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '0.5_1.0' results_1_0.5_1.0_0.2_\[0\,\ 0\] results_2_0.5_1.0_0.2_\[0\,\ 0\] results_3_0.5_1.0_0.2_\[0\,\ 0\] results_4_0.5_1.0_0.2_\[0\,\ 0\] results_5_0.5_1.0_0.2_\[0\,\ 0\]

~/catkin_ws/src/gitagent/result_scripts/plot_3.py dynamic '1.0_1.0' results_1_1.0_1.0_0.2_\[0\,\ 0\] results_2_1.0_1.0_0.2_\[0\,\ 0\] results_3_1.0_1.0_0.2_\[0\,\ 0\] results_4_1.0_1.0_0.2_\[0\,\ 0\] results_5_1.0_1.0_0.2_\[0\,\ 0\]


~/catkin_ws/src/gitagent/result_scripts/heatmap.py dynamic dynamic_total
mv dynamicall_heatmap.jpg all_mem_0_2.jpg
mv dynamicdepend_heatmap.jpg depend_mem_0_2.jpg

find . -name '*.jpg' | zip dynamic_mem_0.2.zip -@
~/catkin_ws/src/gitagent/result_scripts/send.sh dynamic_mem_0.2.zip

cd ~/catkin_ws/
