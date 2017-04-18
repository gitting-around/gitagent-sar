cd ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.125/

chmod a+x plot_2.py heatmap.py

./plot_2.py dynamic '0.0_0.0' results_1_0.0_0.0_0.125_\[0\,\ 0\] results_2_0.0_0.0_0.125_\[0\,\ 0\] results_3_0.0_0.0_0.125_\[0\,\ 0\] results_4_0.0_0.0_0.125_\[0\,\ 0\] results_5_0.0_0.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.0' results_1_0.5_0.0_0.125_\[0\,\ 0\] results_2_0.5_0.0_0.125_\[0\,\ 0\] results_3_0.5_0.0_0.125_\[0\,\ 0\] results_4_0.5_0.0_0.125_\[0\,\ 0\] results_5_0.5_0.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.0' results_1_1.0_0.0_0.125_\[0\,\ 0\] results_2_1.0_0.0_0.125_\[0\,\ 0\] results_3_1.0_0.0_0.125_\[0\,\ 0\] results_4_1.0_0.0_0.125_\[0\,\ 0\] results_5_1.0_0.0_0.125_\[0\,\ 0\]


./plot_2.py dynamic '0.0_0.5' results_1_0.0_0.5_0.125_\[0\,\ 0\] results_2_0.0_0.5_0.125_\[0\,\ 0\] results_3_0.0_0.5_0.125_\[0\,\ 0\] results_4_0.0_0.5_0.125_\[0\,\ 0\] results_5_0.0_0.5_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.5' results_1_0.5_0.5_0.125_\[0\,\ 0\] results_2_0.5_0.5_0.125_\[0\,\ 0\] results_3_0.5_0.5_0.125_\[0\,\ 0\] results_4_0.5_0.5_0.125_\[0\,\ 0\] results_5_0.5_0.5_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.5' results_1_1.0_0.5_0.125_\[0\,\ 0\] results_2_1.0_0.5_0.125_\[0\,\ 0\] results_3_1.0_0.5_0.125_\[0\,\ 0\] results_4_1.0_0.5_0.125_\[0\,\ 0\] results_5_1.0_0.5_0.125_\[0\,\ 0\]


./plot_2.py dynamic '0.0_1.0' results_1_0.0_1.0_0.125_\[0\,\ 0\] results_2_0.0_1.0_0.125_\[0\,\ 0\] results_3_0.0_1.0_0.125_\[0\,\ 0\] results_4_0.0_1.0_0.125_\[0\,\ 0\] results_5_0.0_1.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_1.0' results_1_0.5_1.0_0.125_\[0\,\ 0\] results_2_0.5_1.0_0.125_\[0\,\ 0\] results_3_0.5_1.0_0.125_\[0\,\ 0\] results_4_0.5_1.0_0.125_\[0\,\ 0\] results_5_0.5_1.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_1.0' results_1_1.0_1.0_0.125_\[0\,\ 0\] results_2_1.0_1.0_0.125_\[0\,\ 0\] results_3_1.0_1.0_0.125_\[0\,\ 0\] results_4_1.0_1.0_0.125_\[0\,\ 0\] results_5_1.0_1.0_0.125_\[0\,\ 0\]


./heatmap.py dynamic dynamic_total

mv dynamic_total dynamic_total_old

find . -name '.jpg*' | zip dynamic_nomem_0.125.zip -@
./send.sh

cd ~/catkin_ws/results/braitenberg_1/dynamic/nomem/pressure_0.2/

chmod a+x plot_2.py heatmap.py

./plot_2.py dynamic '0.0_0.0' results_1_0.0_0.0_0.2_\[0\,\ 0\] results_2_0.0_0.0_0.2_\[0\,\ 0\] results_3_0.0_0.0_0.2_\[0\,\ 0\] results_4_0.0_0.0_0.2_\[0\,\ 0\] results_5_0.0_0.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.0' results_1_0.5_0.0_0.2_\[0\,\ 0\] results_2_0.5_0.0_0.2_\[0\,\ 0\] results_3_0.5_0.0_0.2_\[0\,\ 0\] results_4_0.5_0.0_0.2_\[0\,\ 0\] results_5_0.5_0.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.0' results_1_1.0_0.0_0.2_\[0\,\ 0\] results_2_1.0_0.0_0.2_\[0\,\ 0\] results_3_1.0_0.0_0.2_\[0\,\ 0\] results_4_1.0_0.0_0.2_\[0\,\ 0\] results_5_1.0_0.0_0.2_\[0\,\ 0\]


./plot_2.py dynamic '0.0_0.5' results_1_0.0_0.5_0.2_\[0\,\ 0\] results_2_0.0_0.5_0.2_\[0\,\ 0\] results_3_0.0_0.5_0.2_\[0\,\ 0\] results_4_0.0_0.5_0.2_\[0\,\ 0\] results_5_0.0_0.5_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.5' results_1_0.5_0.5_0.2_\[0\,\ 0\] results_2_0.5_0.5_0.2_\[0\,\ 0\] results_3_0.5_0.5_0.2_\[0\,\ 0\] results_4_0.5_0.5_0.2_\[0\,\ 0\] results_5_0.5_0.5_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.5' results_1_1.0_0.5_0.2_\[0\,\ 0\] results_2_1.0_0.5_0.2_\[0\,\ 0\] results_3_1.0_0.5_0.2_\[0\,\ 0\] results_4_1.0_0.5_0.2_\[0\,\ 0\] results_5_1.0_0.5_0.2_\[0\,\ 0\]


./plot_2.py dynamic '0.0_1.0' results_1_0.0_1.0_0.2_\[0\,\ 0\] results_2_0.0_1.0_0.2_\[0\,\ 0\] results_3_0.0_1.0_0.2_\[0\,\ 0\] results_4_0.0_1.0_0.2_\[0\,\ 0\] results_5_0.0_1.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_1.0' results_1_0.5_1.0_0.2_\[0\,\ 0\] results_2_0.5_1.0_0.2_\[0\,\ 0\] results_3_0.5_1.0_0.2_\[0\,\ 0\] results_4_0.5_1.0_0.2_\[0\,\ 0\] results_5_0.5_1.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_1.0' results_1_1.0_1.0_0.2_\[0\,\ 0\] results_2_1.0_1.0_0.2_\[0\,\ 0\] results_3_1.0_1.0_0.2_\[0\,\ 0\] results_4_1.0_1.0_0.2_\[0\,\ 0\] results_5_1.0_1.0_0.2_\[0\,\ 0\]


./heatmap.py dynamic dynamic_total

find . -name '.jpg*' | zip dynamic_nomem_0.2.zip -@
./send.sh



cd ~/catkin_ws/results/braitenberg_1/static/pressure_0.125/

chmod a+x plot_2.py heatmap.py

./plot_2.py static '0.0_0.0' results_1_0.0_0.0_0.125_\[1\,\ 1\] results_2_0.0_0.0_0.125_\[1\,\ 1\] results_3_0.0_0.0_0.125_\[1\,\ 1\] results_4_0.0_0.0_0.125_\[1\,\ 1\] results_5_0.0_0.0_0.125_\[1\,\ 1\]

./plot_2.py static '0.5_0.0' results_1_0.5_0.0_0.125_\[1\,\ 1\] results_2_0.5_0.0_0.125_\[1\,\ 1\] results_3_0.5_0.0_0.125_\[1\,\ 1\] results_4_0.5_0.0_0.125_\[1\,\ 1\] results_5_0.5_0.0_0.125_\[1\,\ 1\]

./plot_2.py static '1.0_0.0' results_1_1.0_0.0_0.125_\[1\,\ 1\] results_2_1.0_0.0_0.125_\[1\,\ 1\] results_3_1.0_0.0_0.125_\[1\,\ 1\] results_4_1.0_0.0_0.125_\[1\,\ 1\] results_5_1.0_0.0_0.125_\[1\,\ 1\]


./plot_2.py static '0.0_0.5' results_1_0.0_0.5_0.125_\[1\,\ 1\] results_2_0.0_0.5_0.125_\[1\,\ 1\] results_3_0.0_0.5_0.125_\[1\,\ 1\] results_4_0.0_0.5_0.125_\[1\,\ 1\] results_5_0.0_0.5_0.125_\[1\,\ 1\]

./plot_2.py static '0.5_0.5' results_1_0.5_0.5_0.125_\[1\,\ 1\] results_2_0.5_0.5_0.125_\[1\,\ 1\] results_3_0.5_0.5_0.125_\[1\,\ 1\] results_4_0.5_0.5_0.125_\[1\,\ 1\] results_5_0.5_0.5_0.125_\[1\,\ 1\]

./plot_2.py static '1.0_0.5' results_1_1.0_0.5_0.125_\[1\,\ 1\] results_2_1.0_0.5_0.125_\[1\,\ 1\] results_3_1.0_0.5_0.125_\[1\,\ 1\] results_4_1.0_0.5_0.125_\[0\,\ 0\] results_5_1.0_0.5_0.125_\[1\,\ 1\]


./plot_2.py static '0.0_1.0' results_1_0.0_1.0_0.125_\[1\,\ 1\] results_2_0.0_1.0_0.125_\[1\,\ 1\] results_3_0.0_1.0_0.125_\[1\,\ 1\] results_4_0.0_1.0_0.125_\[1\,\ 1\] results_5_0.0_1.0_0.125_\[1\,\ 1\]

./plot_2.py static '0.5_1.0' results_1_0.5_1.0_0.125_\[1\,\ 1\] results_2_0.5_1.0_0.125_\[1\,\ 1\] results_3_0.5_1.0_0.125_\[1\,\ 1\] results_4_0.5_1.0_0.125_\[1\,\ 1\] results_5_0.5_1.0_0.125_\[1\,\ 1\]

./plot_2.py static '1.0_1.0' results_1_1.0_1.0_0.125_\[1\,\ 1\] results_2_1.0_1.0_0.125_\[1\,\ 1\] results_3_1.0_1.0_0.125_\[1\,\ 1\] results_4_1.0_1.0_0.125_\[1\,\ 1\] results_5_1.0_1.0_0.125_\[1\,\ 1\]


./heatmap.py static static_total

mv static_total static_total_old

find . -name '.jpg*' | zip static_nomem_0.125.zip -@
./send.sh

cd ~/catkin_ws/results/braitenberg_1/static/pressure_0.2/

chmod a+x plot_2.py heatmap.py

./plot_2.py static '0.0_0.0' results_1_0.0_0.0_0.2_\[1\,\ 1\] results_2_0.0_0.0_0.2_\[1\,\ 1\] results_3_0.0_0.0_0.2_\[1\,\ 1\] results_4_0.0_0.0_0.2_\[1\,\ 1\] results_5_0.0_0.0_0.2_\[1\,\ 1\]

./plot_2.py static '0.5_0.0' results_1_0.5_0.0_0.2_\[1\,\ 1\] results_2_0.5_0.0_0.2_\[1\,\ 1\] results_3_0.5_0.0_0.2_\[1\,\ 1\] results_4_0.5_0.0_0.2_\[1\,\ 1\] results_5_0.5_0.0_0.2_\[1\,\ 1\]

./plot_2.py static '1.0_0.0' results_1_1.0_0.0_0.2_\[1\,\ 1\] results_2_1.0_0.0_0.2_\[1\,\ 1\] results_3_1.0_0.0_0.2_\[1\,\ 1\] results_4_1.0_0.0_0.2_\[1\,\ 1\] results_5_1.0_0.0_0.2_\[1\,\ 1\]


./plot_2.py static '0.0_0.5' results_1_0.0_0.5_0.2_\[1\,\ 1\] results_2_0.0_0.5_0.2_\[1\,\ 1\] results_3_0.0_0.5_0.2_\[1\,\ 1\] results_4_0.0_0.5_0.2_\[1\,\ 1\] results_5_0.0_0.5_0.2_\[1\,\ 1\]

./plot_2.py static '0.5_0.5' results_1_0.5_0.5_0.2_\[1\,\ 1\] results_2_0.5_0.5_0.2_\[1\,\ 1\] results_3_0.5_0.5_0.2_\[1\,\ 1\] results_4_0.5_0.5_0.2_\[1\,\ 1\] results_5_0.5_0.5_0.2_\[1\,\ 1\]

./plot_2.py static '1.0_0.5' results_1_1.0_0.5_0.2_\[1\,\ 1\] results_2_1.0_0.5_0.2_\[1\,\ 1\] results_3_1.0_0.5_0.2_\[1\,\ 1\] results_4_1.0_0.5_0.2_\[1\,\ 1\] results_5_1.0_0.5_0.2_\[1\,\ 1\]


./plot_2.py static '0.0_1.0' results_1_0.0_1.0_0.2_\[1\,\ 1\] results_2_0.0_1.0_0.2_\[1\,\ 1\] results_3_0.0_1.0_0.2_\[1\,\ 1\] results_4_0.0_1.0_0.2_\[1\,\ 1\] results_5_0.0_1.0_0.2_\[1\,\ 1\]

./plot_2.py static '0.5_1.0' results_1_0.5_1.0_0.2_\[1\,\ 1\] results_2_0.5_1.0_0.2_\[1\,\ 1\] results_3_0.5_1.0_0.2_\[1\,\ 1\] results_4_0.5_1.0_0.2_\[1\,\ 1\] results_5_0.5_1.0_0.2_\[1\,\ 1\]

./plot_2.py static '1.0_1.0' results_1_1.0_1.0_0.2_\[1\,\ 1\] results_2_1.0_1.0_0.2_\[1\,\ 1\] results_3_1.0_1.0_0.2_\[1\,\ 1\] results_4_1.0_1.0_0.2_\[1\,\ 1\] results_5_1.0_1.0_0.2_\[1\,\ 1\]


./heatmap.py static static_total

find . -name '.jpg*' | zip static_nomem_0.2.zip -@
./send.sh



cd ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.125/

chmod a+x plot_2.py heatmap.py

./plot_2.py dynamic '0.0_0.0' results_1_0.0_0.0_0.125_\[0\,\ 0\] results_2_0.0_0.0_0.125_\[0\,\ 0\] results_3_0.0_0.0_0.125_\[0\,\ 0\] results_4_0.0_0.0_0.125_\[0\,\ 0\] results_5_0.0_0.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.0' results_1_0.5_0.0_0.125_\[0\,\ 0\] results_2_0.5_0.0_0.125_\[0\,\ 0\] results_3_0.5_0.0_0.125_\[0\,\ 0\] results_4_0.5_0.0_0.125_\[0\,\ 0\] results_5_0.5_0.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.0' results_1_1.0_0.0_0.125_\[0\,\ 0\] results_2_1.0_0.0_0.125_\[0\,\ 0\] results_3_1.0_0.0_0.125_\[0\,\ 0\] results_4_1.0_0.0_0.125_\[0\,\ 0\] results_5_1.0_0.0_0.125_\[0\,\ 0\]


./plot_2.py dynamic '0.0_0.5' results_1_0.0_0.5_0.125_\[0\,\ 0\] results_2_0.0_0.5_0.125_\[0\,\ 0\] results_3_0.0_0.5_0.125_\[0\,\ 0\] results_4_0.0_0.5_0.125_\[0\,\ 0\] results_5_0.0_0.5_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.5' results_1_0.5_0.5_0.125_\[0\,\ 0\] results_2_0.5_0.5_0.125_\[0\,\ 0\] results_3_0.5_0.5_0.125_\[0\,\ 0\] results_4_0.5_0.5_0.125_\[0\,\ 0\] results_5_0.5_0.5_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.5' results_1_1.0_0.5_0.125_\[0\,\ 0\] results_2_1.0_0.5_0.125_\[0\,\ 0\] results_3_1.0_0.5_0.125_\[0\,\ 0\] results_4_1.0_0.5_0.125_\[0\,\ 0\] results_5_1.0_0.5_0.125_\[0\,\ 0\]


./plot_2.py dynamic '0.0_1.0' results_1_0.0_1.0_0.125_\[0\,\ 0\] results_2_0.0_1.0_0.125_\[0\,\ 0\] results_3_0.0_1.0_0.125_\[0\,\ 0\] results_4_0.0_1.0_0.125_\[0\,\ 0\] results_5_0.0_1.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '0.5_1.0' results_1_0.5_1.0_0.125_\[0\,\ 0\] results_2_0.5_1.0_0.125_\[0\,\ 0\] results_3_0.5_1.0_0.125_\[0\,\ 0\] results_4_0.5_1.0_0.125_\[0\,\ 0\] results_5_0.5_1.0_0.125_\[0\,\ 0\]

./plot_2.py dynamic '1.0_1.0' results_1_1.0_1.0_0.125_\[0\,\ 0\] results_2_1.0_1.0_0.125_\[0\,\ 0\] results_3_1.0_1.0_0.125_\[0\,\ 0\] results_4_1.0_1.0_0.125_\[0\,\ 0\] results_5_1.0_1.0_0.125_\[0\,\ 0\]


./heatmap.py dynamic dynamic_total

mv dynamic_total dynamic_total_old

find . -name '.jpg*' | zip dynamic_mem_0.125.zip -@
./send.sh

cd ~/catkin_ws/results/braitenberg_1/dynamic/mem/pressure_0.2/

chmod a+x plot_2.py heatmap.py

./plot_2.py dynamic '0.0_0.0' results_1_0.0_0.0_0.2_\[0\,\ 0\] results_2_0.0_0.0_0.2_\[0\,\ 0\] results_3_0.0_0.0_0.2_\[0\,\ 0\] results_4_0.0_0.0_0.2_\[0\,\ 0\] results_5_0.0_0.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.0' results_1_0.5_0.0_0.2_\[0\,\ 0\] results_2_0.5_0.0_0.2_\[0\,\ 0\] results_3_0.5_0.0_0.2_\[0\,\ 0\] results_4_0.5_0.0_0.2_\[0\,\ 0\] results_5_0.5_0.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.0' results_1_1.0_0.0_0.2_\[0\,\ 0\] results_2_1.0_0.0_0.2_\[0\,\ 0\] results_3_1.0_0.0_0.2_\[0\,\ 0\] results_4_1.0_0.0_0.2_\[0\,\ 0\] results_5_1.0_0.0_0.2_\[0\,\ 0\]


./plot_2.py dynamic '0.0_0.5' results_1_0.0_0.5_0.2_\[0\,\ 0\] results_2_0.0_0.5_0.2_\[0\,\ 0\] results_3_0.0_0.5_0.2_\[0\,\ 0\] results_4_0.0_0.5_0.2_\[0\,\ 0\] results_5_0.0_0.5_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_0.5' results_1_0.5_0.5_0.2_\[0\,\ 0\] results_2_0.5_0.5_0.2_\[0\,\ 0\] results_3_0.5_0.5_0.2_\[0\,\ 0\] results_4_0.5_0.5_0.2_\[0\,\ 0\] results_5_0.5_0.5_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_0.5' results_1_1.0_0.5_0.2_\[0\,\ 0\] results_2_1.0_0.5_0.2_\[0\,\ 0\] results_3_1.0_0.5_0.2_\[0\,\ 0\] results_4_1.0_0.5_0.2_\[0\,\ 0\] results_5_1.0_0.5_0.2_\[0\,\ 0\]


./plot_2.py dynamic '0.0_1.0' results_1_0.0_1.0_0.2_\[0\,\ 0\] results_2_0.0_1.0_0.2_\[0\,\ 0\] results_3_0.0_1.0_0.2_\[0\,\ 0\] results_4_0.0_1.0_0.2_\[0\,\ 0\] results_5_0.0_1.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '0.5_1.0' results_1_0.5_1.0_0.2_\[0\,\ 0\] results_2_0.5_1.0_0.2_\[0\,\ 0\] results_3_0.5_1.0_0.2_\[0\,\ 0\] results_4_0.5_1.0_0.2_\[0\,\ 0\] results_5_0.5_1.0_0.2_\[0\,\ 0\]

./plot_2.py dynamic '1.0_1.0' results_1_1.0_1.0_0.2_\[0\,\ 0\] results_2_1.0_1.0_0.2_\[0\,\ 0\] results_3_1.0_1.0_0.2_\[0\,\ 0\] results_4_1.0_1.0_0.2_\[0\,\ 0\] results_5_1.0_1.0_0.2_\[0\,\ 0\]


./heatmap.py dynamic dynamic_total

find . -name '.jpg*' | zip dynamic_mem_0.2.zip -@
./send.sh
