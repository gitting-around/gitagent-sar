#!/usr/bin/env python
import sys
from numpy import *
import matplotlib.pyplot as plt;

plt.rcdefaults()
import matplotlib.pyplot as plt
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
    print ave_tasks
    # Plot Bar Plots.

    # add completion rate to file.
    outname = dynamic + '_' + 'total'
    with open(outname, 'w+') as out:
        out.write(str(ave_tasks[2]/float(ave_tasks[0])) + ' ' + str(ave_tasks[3]/float(ave_tasks[1])) + '\n')

    fig = plt.figure()

    objects = ('ta', 'tda', 'tc', 'tdc', 'sta', 'std', 'cn', 'req', 'req_s', 'req_r', 'req_r_a', 'req_acc')
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
        for point in points:
            if point[0] == '0':
                color = 'green'
                marker = 'x'
            else:
                color = 'blue'
                marker = 'o'
            plt.plot(i, float(point[1]), c=color, marker=marker)
            plt.plot(i, float(point[3]), c='red', marker=marker)
            i += 1
        no = no + 1
        fig.savefig(str(no) +'_' + case_name + '_tasks_ave.jpg')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ./plot_2.py static/dynamic case_name filename'
        sys.exit()

    name_of_files = []
    for x in range(3, len(sys.argv)):
        name_of_files.append(sys.argv[x])

    population_plot(sys.argv[1], sys.argv[2], name_of_files)
    plot_delta_gamma(sys.argv[1], name_of_files)
