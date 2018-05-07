#!/usr/bin/env python
import sys
from numpy import *
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import datetime
import time

def population_plot(case_name, dynamic, fnames, row_idx, part):
    tasks = []
    ave_runtime = 0.0
    for fname in fnames:
        with open(fname, 'r') as f:
            lines = f.readlines()
            tasks.append(map(float, filter(None, lines[0].strip().split(' '))))
            ave_runtime = float(lines[8].split(' ')[2])
            #ave_runtime = time.strptime(lines[8].split(' ')[2], '%H:%M:%S')
            #ave_runtime = datetime.timedelta(hours=ave_runtime.tm_hour,minutes=ave_runtime.tm_min,seconds=ave_runtime.tm_sec).total_seconds()

    # print tasks

    i = 0
    simple_tasks = []
    while i < len(tasks):
    #while i < 1:
        j = 0
        simple_tasks.append([])
        #print tasks[i]
        #print len(tasks[i])
        while j < len(tasks[i]):
            if j < len(tasks[i])-4:
                #print sum(tasks[i][j:j + 3])
                simple_tasks[i].append(sum(tasks[i][j:j + 3]))
                #print "res"
                #print simple_tasks[i]
                j += 3
            else:
                simple_tasks[i].append(tasks[i][j])
                j += 1
        print simple_tasks[i]
        i += 1

    print simple_tasks
    # Calculate averages over fnames
    simple_tasks = np.array(simple_tasks)
    ave_tasks = np.sum(simple_tasks, axis=0)

    # Ignore noones - that is request/attempts when noone was known
    ave_tasks[0] = ave_tasks[0] - ave_tasks[6]
    ave_tasks[1] = ave_tasks[1] - ave_tasks[6]
    ave_tasks[4] = ave_tasks[4] - ave_tasks[6]
    print "len: " + str(len(ave_tasks))
    # Put ta,tc,tda,tdc,req_,req_acc,req_suc to file
    # <delta,gamma> ta tc trate tda tdc tdrate req req_acc req_succ
    result = []
    with open("results_final") as f:
        lines = f.readlines()
        result =map(int, filter(None, lines[row_idx].strip().split(' ')))
    print result
    print case_name
    case = [x for x in case_name.split('_')]
    sim_time = 600.0 #10m
    num_fires = 40.0

    with open(dynamic + '_tabular', 'a') as out:
        if not ave_tasks[0] == 0:
            t1 = ave_tasks[2] / float(ave_tasks[0])
        else:
            t1 = -1.0

        if not ave_tasks[1] == 0:
            t2 = ave_tasks[3] / float(ave_tasks[1])
        else:
            t2 = -1.0
        if part == 1:
            out.write(
            '$\langle' + str(case[0]) + ',' + str(case[1]) + '\\rangle$& ' + '$' + str(int(ave_tasks[0]))+ '$&' + ' $' + str(int(ave_tasks[2])) + '$&$ ' + str(
                round(t1,2)) + '$&$  ' + str(int(ave_tasks[1])) + '$&$  ' + str(int(ave_tasks[3])) + '$&$  ' + str(round(t2,2)) + '$&$  ' 
                + str(round(result[0]/float(num_fires),2))+ '$&$  ' + str(round(result[1]/float(result[2]),2)) +'$\\\\\n')

            with open(dynamic + '_score', 'a') as out1:
                if ave_tasks[2] == 0:
                    ch_tc = 0.0
                else:
                    ch_tc = 1 - round(ave_tasks[17]/float(ave_tasks[2]),2) 
                    
                if t1 == -1:
                    t1 = 0
                if t2 == -1:
                    t2 = 0
                score = (round(t1,2) + round(t2,2) + 1 - round(ave_runtime/float(sim_time),2) + round(result[0]/float(num_fires),2) + round(result[1]/float(result[2]),2)
                + 1 - round(ave_tasks[2]/float(ave_tasks[15]),2))/float(6)

                out1.write(
            '$\langle' + str(case[0]) + ',' + str(case[1]) + '\\rangle$& ' + '$' + str(round(score,2))+'$\\\\\n')
        else:
            out.write(
            '$\langle' + str(case[0]) + ',' + str(case[1]) + '\\rangle$& ' + '$' + str(
                int(ave_tasks[7])) + '$&$  ' + str(int(ave_tasks[8])) + '$&$  ' + str(int(ave_tasks[9])) + '$&$  ' + str(
                int(ave_tasks[10])) + ' $&$ ' + str(int(ave_tasks[11])) + '$&$  ' + str(int(ave_tasks[14]))+ '$&$  ' + str(round(ave_runtime/float(sim_time),2)) 
                + ' $&$'+str(round(ave_tasks[2]/float(ave_tasks[15]),2))+ ' $&$'+str(int(ave_tasks[16]))+ ' $&$'+str(int(ave_tasks[17]))+'$\\\\\n')

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

        plt.subplot(2, 1, 1)
        plt.plot(np.arange(len(delta)), delta, c='green')
        axes = plt.gca()
        axes.set_ylim([-0.5, 1.5])

        plt.plot(np.arange(len(delta)), delta_p, c='red')
        axes = plt.gca()
        axes.set_ylim([-0.5, 1.5])

        plt.subplot(2, 1, 2)
        plt.plot(np.arange(len(gamma)), gamma, c='blue')
        axes = plt.gca()
        axes.set_ylim([-0.5, 1.5])

        plt.plot(np.arange(len(gamma)), gamma_p, c='red')
        axes = plt.gca()
        axes.set_ylim([-0.5, 1.5])

        no = no + 1
        plt.suptitle("All tasks")
        fig.savefig(str(no) + '_' + case_name + '_all_delta_gamma_mu.jpg')

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

        #fig.savefig(str(no) + '_' + case_name + '_depend_delta_gamma_mu.jpg')

        #fig = plt.figure()
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

        #plt.suptitle("Own tasks")

        #fig.savefig(str(no) + '_' + case_name + '_own_delta_gamma_mu.jpg')


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Usage: ./plot_2.py static/dynamic case_name row_idx part1/2 filename'
        sys.exit()

    name_of_files = []
    for x in range(5, len(sys.argv)):
        name_of_files.append(sys.argv[x])
    print sys.argv[4]
    population_plot(sys.argv[2], sys.argv[1], name_of_files, int(sys.argv[3]), int(sys.argv[4]))
    #plot_delta_gamma(sys.argv[2], name_of_files)
