#!/usr/bin/env python
import sys
from numpy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np


def population_plot(case_name, dynamic, fnames):
    tasks = []
    for fname in fnames:
        with open(fname, 'r') as f:
            lines = f.readlines()
            tasks.append(map(float, filter(None, lines[0].strip().split(' '))))

    # print tasks

    i = 0
    simple_tasks = []
    while i < len(tasks):
        j = 0
        simple_tasks.append([])
        while j < len(tasks[i]):
            simple_tasks[i].append(sum(tasks[i][j:j + 3]))
            j += 3
        print simple_tasks[i]
        i += 1

    print simple_tasks
    # Calculate averages over fnames
    simple_tasks = np.array(simple_tasks)
    ave_tasks = np.sum(simple_tasks, axis=0)

    #Ignore noones - that is request/attempts when noone was known
    ave_tasks[0] = ave_tasks[0] - ave_tasks[6]
    ave_tasks[1] = ave_tasks[1] - ave_tasks[6]
    ave_tasks[4] = ave_tasks[4] - ave_tasks[6]
    print ave_tasks
    # Plot Bar Plots.
    
    # add completion rate to file.
    outname = dynamic + '_' + 'total'
    t3 = [float(x) for x in case_name.split('_')]
    with open(outname, 'a') as out:
	if not ave_tasks[0] == 0:
	    t1 = ave_tasks[2]/float(ave_tasks[0])
	else:
	    t1 = -1.0

	if not ave_tasks[1] == 0:
	    t2 = ave_tasks[3]/float(ave_tasks[1])
	else:
	    t2 = -1.0

        out.write(str(t3[0]) + ' ' + str(t3[1]) + ' ' + str(t1) + ' ' + str(t2) + '\n')

    fig = plt.figure()

    objects = ('ta', 'tda', 'tc', 'tdc', 'sta', 'stc', 'cn', 'req', 'r_s', 'r_r', 'r_ra', 'r_rs')
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, ave_tasks, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Value')
    plt.title('Preliminary')

    fig.savefig(case_name+'_tasks_ave.jpg')


def plot_delta_gamma(case_name, fnames):
    pieces = []
    for fname in fnames:
        with open(fname, 'r') as f:
            lines = f.readlines()
            pieces.append(filter(None, lines[6].strip().split(',')))

    no = 0
    for y in pieces:
        points = []
        for x in y:
            points.append(filter(None, x.split(' ')))
        # print points
        # Plot the points
        fig = plt.figure()
        i = 0
        gamma = []
        delta = []
        gamma_p = []
        delta_p = []
        for point in points:
            if point[0] == '0':
                delta.append(float(point[1]))
                delta_p.append(float(point[3]))
            else:
                gamma.append(float(point[1]))
                gamma_p.append(float(point[3]))
            i += 1   
        
        delta = np.array(delta)
        delta_p = np.array(delta_p)
        gamma = np.array(gamma)
        gamma_p = np.array(gamma_p) 

        plt.subplot(2,1,1)
        plt.plot(np.arange(len(delta)), delta, c='green')
        axes = plt.gca()
        axes.set_ylim([-0.5,1.5]) 
        
        plt.plot(np.arange(len(delta)), delta_p, c='red')
        axes = plt.gca()
        axes.set_ylim([-0.5,1.5]) 
        
        plt.subplot(2,1,2)
        plt.plot(np.arange(len(gamma)), gamma, c='blue')
        axes = plt.gca()
        axes.set_ylim([-0.5,1.5]) 
        
        plt.plot(np.arange(len(gamma)), gamma_p, c='red')
        axes = plt.gca()
        axes.set_ylim([-0.5,1.5]) 

        no = no + 1
        plt.suptitle("All tasks")
        fig.savefig(str(no) +'_' + case_name + '_all_delta_gamma_mu.jpg')

        fig = plt.figure()
        i = 0

        for point in points:
            if point[0] == '0':
                color = 'green'
                marker = 'x'
            else:
                color = 'blue'
                marker = 'o'
            plt.plot(i, float(point[1]), c=color, marker=marker)
            plt.plot(i, float(point[4]), c='red', marker=marker)
            i += 1
        
        plt.suptitle("Depend tasks")

        fig.savefig(str(no) +'_' + case_name + '_depend_delta_gamma_mu.jpg')


        fig = plt.figure()
        i = 0

        for point in points:
            if point[0] == '0':
                color = 'green'
                marker = 'x'
            else:
                color = 'blue'
                marker = 'o'
            plt.plot(i, float(point[1]), c=color, marker=marker)
            plt.plot(i, float(point[5]), c='red', marker=marker)
            i += 1
      
        plt.suptitle("Own tasks")

        fig.savefig(str(no) +'_' + case_name + '_own_delta_gamma_mu.jpg')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ./plot_2.py static/dynamic case_name filename'
        sys.exit()

    name_of_files = []
    for x in range(3, len(sys.argv)):
        name_of_files.append(sys.argv[x])

    population_plot(sys.argv[2], sys.argv[1], name_of_files)
    plot_delta_gamma(sys.argv[2], name_of_files)
