#!/usr/bin/env bash
timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_1\|0_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/1_0/ \;


timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_0\|1_mem0.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/nomem/0_1/ \;



timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_1\|0_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/1_0/ \;


timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_0\|1_mem1.launch
find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/mixed/mem/0_1/ \;
