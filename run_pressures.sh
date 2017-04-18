#!/usr/bin/env bash
timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/ \;


timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_0\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/ \;



timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/ \;


timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_1\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/ \;



timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.125_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/ \;


timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.2_0\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/ \;
