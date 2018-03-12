#!/usr/bin/env python
import time

class Logging:
    def __init__(self, popSize, provaNr, ID, delta, depend_nr):
        self.stdout_log = '/home/mfi01/catkin_ws/results/' + 'stdout_' + str(ID) + '_' + time.strftime("%H:%M", time.gmtime(time.time())) + '_'
        self.stdout_callback = '/home/mfi01/catkin_ws/results/' + 'stdout_' + str(ID) + '_' + time.strftime("%H:%M", time.gmtime(time.time())) + '_callback'
        self.stdout_handle = '/home/mfi01/catkin_ws/results/' + 'stdout_' + str(ID) + '_' + time.strftime("%H:%M", time.gmtime(time.time())) + '_'

    # Write to file ~ the cost of calling the procedure multiple times is not cared for at this moment
    def write_log_file(self, filename, data):
        with open(filename, 'a+') as f:
            f.write(data)
