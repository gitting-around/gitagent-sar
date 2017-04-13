#!/usr/bin/env bash
timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_0.5_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.0_1.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_0.5_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_0.5_1.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_0.5_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;

timeout 32m roslaunch ~/catkin_ws/src/gitagent/Launch/launch_agents_5_1.0_1.0_0.05_0\|0_mem1.launch
find . -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/braitenberg_1/dynamic/mem \;
