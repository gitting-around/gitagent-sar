#!/usr/bin/env bash

source devel/setup.bash
cd ~/catkin_ws/
SIMULATION_RAND=0
echo $SIMULATION_RAND
export SIMULATION_RAND
printenv | grep SIMULATION_RAND

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_0\|0_env.launch


roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_1\|1_env.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_1\|1_env.launch

SIMULATION_RAND=1
#gamma, delta notation in the launch file does not matter 
#values will be set from text file, because simulation_rand = 1
roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env.launch

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env.launch

find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/sandr/w\=25\,v\=5/trial$1 \;
cd ~/catkin_ws/results/sandr/w\=25\,v\=5/trial$1
../../aamas-res.sh 1
../../aamas-res.sh 2
mv dynamic_score dynamic_w\=25\,v\=5_score
mv static_score static_w\=25\,v\=5_score
mv dynamic_tabular dynamic_w\=25\,v\=5_tabular
mv static_tabular static_w\=25\,v\=5_tabular
zip -r logs_$1_1.zip ~/catkin_ws/results/stdout*
rm ~/catkin_ws/results/stdout*
rosclean purge -y
cd ~/catkin_ws/

SIMULATION_RAND=0
echo $SIMULATION_RAND
export SIMULATION_RAND
printenv | grep SIMULATION_RAND

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_0\|0_env2.launch


roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_1\|1_env2.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_1\|1_env2.launch

SIMULATION_RAND=1
#gamma, delta notation in the launch file does not matter 
#values will be set from text file, because simulation_rand = 1
roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env2.launch

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env2.launch

find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/sandr/w\=50\,v\=10/trial$1 \;
cd ~/catkin_ws/results/sandr/w\=50\,v\=10/trial$1
../../aamas-res.sh 1
../../aamas-res.sh 2
mv dynamic_score dynamic_w\=50\,v\=10_score
mv static_score static_w\=50\,v\=10_score
mv dynamic_tabular dynamic_w\=50\,v\=10_tabular
mv static_tabular static_w\=50\,v\=10_tabular
zip -r logs_$1_2.zip ~/catkin_ws/results/stdout*
rm ~/catkin_ws/results/stdout*
rosclean purge -y
cd ~/catkin_ws/

SIMULATION_RAND=0
echo $SIMULATION_RAND
export SIMULATION_RAND
printenv | grep SIMULATION_RAND

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_0\|0_env3.launch


roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_1\|1_env3.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_1\|1_env3.launch

SIMULATION_RAND=1
#gamma, delta notation in the launch file does not matter 
#values will be set from text file, because simulation_rand = 1
roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env3.launch

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env3.launch

find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/sandr/w\=75\,v\=15/trial$1 \;
cd ~/catkin_ws/results/sandr/w\=75\,v\=15/trial$1
../../aamas-res.sh 1
../../aamas-res.sh 2
mv dynamic_score dynamic_w\=75\,v\=15_score
mv static_score static_w\=75\,v\=15_score
mv dynamic_tabular dynamic_w\=75\,v\=15_tabular
mv static_tabular static_w\=75\,v\=15_tabular
zip -r logs_$1_3.zip ~/catkin_ws/results/stdout*
rm ~/catkin_ws/results/stdout*
rosclean purge -y
cd ~/catkin_ws/

SIMULATION_RAND=0
echo $SIMULATION_RAND
export SIMULATION_RAND
printenv | grep SIMULATION_RAND

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_0\|0_env4.launch


roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.0_0.5_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.5_1.0_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.5_0.5_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.2_0.8_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.2_0.5_0.05_1\|1_env4.launch

roslaunch gitagent launch_agents_20_0.5_0.8_0.05_1\|1_env4.launch

SIMULATION_RAND=1
#gamma, delta notation in the launch file does not matter 
#values will be set from text file, because simulation_rand = 1
roslaunch gitagent launch_agents_20_0.0_1.0_0.05_0\|0_env4.launch

roslaunch gitagent launch_agents_20_0.0_1.0_0.05_1\|1_env4.launch

find . -name 'result*' -maxdepth 1 -type f -exec mv {} ~/catkin_ws/results/sandr/w\=100\,v\=20/trial$1 \;
cd ~/catkin_ws/results/sandr/w\=100\,v\=20/trial$1
../../aamas-res.sh 1
../../aamas-res.sh 2
mv dynamic_score dynamic_w\=100\,v\=20_score
mv static_score static_w\=100\,v\=20_score
mv dynamic_tabular dynamic_w\=100\,v\=20_tabular
mv static_tabular static_w\=100\,v\=20_tabular

zip -r logs_$1_4.zip ~/catkin_ws/results/stdout*
rm ~/catkin_ws/results/stdout*
rosclean purge -y

cd ~/catkin_ws/results/sandr/

zip results_$1.zip w\=25\,v\=5/trial$1/dynamic* w\=25\,v\=5/trial$1/static* w\=50\,v\=10/trial$1/dynamic* w\=50\,v\=10/trial$1/static* w\=75\,v\=15/trial$1/dynamic* w\=75\,v\=15/trial$1/static* w\=100\,v\=20/trial$1/dynamic* w\=100\,v\=20/trial$1/static*

#./send.sh "boh" results_$1.zip
