#!/usr/bin/env python

import sys
import random

def create_conf(no_tasks, no_res, no_deps, no_subtask):
	no_confs = int(input("Enter number of distinct configuration files: "))

	# The configuration file will contain 20 lines.
	for i in range(1, no_confs + 1):
		filename = "agent_conf_" + str(i)
		with open(filename, 'w+') as f:
			# Select randomly 5 tasks out of 100 -- this value is arbitrary, however it does not matter. At the next step we will work with concrete tasks
			tasks = random.sample(range(1, 100), no_tasks)
			for item in tasks:
				f.write(str(item) + ' ')
			f.write('\n')

			iterations = random.sample(range(1, 1000), no_tasks)
			for item in iterations:
				f.write(str(item) + ' ')
			f.write('\n')

			energy = random.sample(range(1, 10000), no_tasks)
			for item in energy:
				f.write(str(item) + ' ')
			f.write('\n')

			for j in range(1, no_tasks + 1):
				rrisurs = random.sample(range(1, 1000), no_res)
				for item in rrisurs:
					f.write(str(item) + ' ')
				f.write('| ')
			f.write('\n')

			for j in range(1, no_tasks + 1):
				orisurs = random.sample(range(1, 1000), no_res)
				for item in orisurs:
					f.write(str(item) + ' ')
				f.write('| ')
			f.write('\n')

			reward = random.sample(range(1, 10000), no_tasks)
			for item in reward:
				f.write(str(item) + ' ')
			f.write('\n')

			for j in range(1, no_tasks + 1):
				f.write(str(random.randint(0,1)) + ' ')
			f.write('\n')

			#The initial values are not relevant -- the agent will change them
			urgency = random.sample(range(0, 1000), no_tasks)
			for item in urgency:
				f.write(str(item) + ' ')
			f.write('\n')

			#This has to make sense
			est_time = random.sample(range(1, 1000), no_tasks)
			for item in est_time:
				f.write(str(item) + ' ')
			f.write('\n')

			for j in range(1, no_tasks + 1):
				deps = random.sample(range(1, 5), no_deps)
				for item in deps:
					f.write(str(item) + ' ')
				f.write('| ')
			f.write('\n')

			for j in range(1, no_tasks + 1):
				subtask = random.sample(range(1, 5), no_subtask)
				for item in subtask:
					f.write(str(item) + ' ')
				f.write('| ')
			f.write('\n')

if __name__=='__main__':
	no_tasks = 5
	no_res = 5
	no_deps = 3
	no_subtask = 3
	create_conf(no_tasks, no_res, no_deps, no_subtask)

'''
Task_ID:
Iterations:
Energy:
Required_Resources:
Optional_Resources:
Reward:
Permission:
Urgency:
Estimated_Time:
Known_Dependencies:
Sub_Tasks:
Sub_Iterations:
Sub_Energy:
Sub_Required_Resources:
Sub_Optional_Resources:
Sub_Reward:
Sub_Permission:
Sub_Urgency:
Sub_Estimated_Time:
Sub_Known_Dependencies:
'''
