#!/usr/bin/env python
import sys
from numpy import *

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcdefaults()
import Tkinter as Tk
import pandas as pd

import numpy as np
from datetime import datetime
import time
import re

def bar_plot(fnames, config):
    temp = []
    with open(fnames[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
    # order according to increasing gamma, then delta
    # 0.5,0.0 - 1.0,0.0 - 0.5,0.2 - 0.8,0.2 - 0.5,0.5 - 0.8,0.5 - 1.0,0.5 - rand
    dynamic_score = np.array([float(temp[1][1]), float(temp[0][1]), float(temp[5][1]), float(temp[4][1]), 
    float(temp[3][1]), float(temp[6][1]), float(temp[2][1]), float(temp[7][1])])
    print dynamic_score

    temp = []
    with open(fnames[1], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
            print line
            print len(line)

    dynamic_all = np.array( [ float(temp[1][3]), float(temp[0][3]), float(temp[5][3]), float(temp[4][3]), 
    float(temp[3][3]), float(temp[6][3]), float(temp[2][3]), float(temp[7][3]) ] )

    dynamic_depend = np.array( [ float(temp[1][6]), float(temp[0][6]), float(temp[5][6]), float(temp[4][6]), 
    float(temp[3][6]), float(temp[6][6]), float(temp[2][6]), float(temp[7][6]) ] )

    dynamic_fires = np.array( [ float(temp[1][7]), float(temp[0][7]), float(temp[5][7]), float(temp[4][7]), 
    float(temp[3][7]), float(temp[6][7]), float(temp[2][7]), float(temp[7][7]) ] )

    dynamic_victims = np.array( [ float(temp[1][8]), float(temp[0][8]), float(temp[5][8]), float(temp[4][8]), 
    float(temp[3][8]), float(temp[6][8]), float(temp[2][8]), float(temp[7][8]) ] )

    dynamic_time = np.array( [ float(temp[9][7]), float(temp[8][7]), float(temp[13][7]), float(temp[12][7]), 
    float(temp[11][7]), float(temp[14][7]), float(temp[10][7]), float(temp[15][7]) ] )

    dynamic_base = np.array( [ float(temp[9][8]), float(temp[8][8]), float(temp[13][8]), float(temp[12][8]), 
    float(temp[11][8]), float(temp[14][8]), float(temp[10][8]), float(temp[15][8]) ] )

    temp = []
    with open(fnames[2], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
    # order according to increasing gamma, then delta
    # 0.5,0.0 - 1.0,0.0 - 0.5,0.2 - 0.8,0.2 - 0.5,0.5 - 0.8,0.5 - 1.0,0.5 - rand
    static_score = np.array([float(temp[1][1]), float(temp[0][1]), float(temp[5][1]), float(temp[4][1]), 
    float(temp[3][1]), float(temp[6][1]), float(temp[2][1]), float(temp[7][1])])
    print static_score

    temp = []
    with open(fnames[3], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)

    static_all = np.array( [ float(temp[1][3]), float(temp[0][3]), float(temp[5][3]), float(temp[4][3]), 
    float(temp[3][3]), float(temp[6][3]), float(temp[2][3]), float(temp[7][3]) ] )

    static_depend = np.array( [ float(temp[1][6]), float(temp[0][6]), float(temp[5][6]), float(temp[4][6]), 
    float(temp[3][6]), float(temp[6][6]), float(temp[2][6]), float(temp[7][6]) ] )

    static_fires = np.array( [ float(temp[1][7]), float(temp[0][7]), float(temp[5][7]), float(temp[4][7]), 
    float(temp[3][7]), float(temp[6][7]), float(temp[2][7]), float(temp[7][7]) ] )

    static_victims = np.array( [ float(temp[1][8]), float(temp[0][8]), float(temp[5][8]), float(temp[4][8]), 
    float(temp[3][8]), float(temp[6][8]), float(temp[2][8]), float(temp[7][8]) ] )

    static_time = np.array( [ float(temp[9][7]), float(temp[8][7]), float(temp[13][7]), float(temp[12][7]), 
    float(temp[11][7]), float(temp[14][7]), float(temp[10][7]), float(temp[15][7]) ] )

    static_base = np.array( [ float(temp[9][8]), float(temp[8][8]), float(temp[13][8]), float(temp[12][8]), 
    float(temp[11][8]), float(temp[14][8]), float(temp[10][8]), float(temp[15][8]) ] )

    objects = ('<0.5,0.0>', '<1.0,0.0>', '<0.5,0.2>', '<0.8,0.2>', '<0.5,0.5>', '<0.8,0.5>', '<1.0,0.5>', '<rand>')
    #objects = ('all', 'depend', '<fires>', '<victims>', '<time>', '<base>', '<score>')
    x_pos = np.arange(len(objects)) * 10
    print x_pos
    offset = 0.1
    w = 0.5

    data = np.transpose(np.array([dynamic_all,static_all, dynamic_depend, static_depend, dynamic_fires, static_fires, 
    dynamic_victims, static_victims, dynamic_time, static_time, dynamic_base, static_base, dynamic_score, static_score]))
    indexes = np.array(['<0.5,0.0>', '<1.0,0.0>', '<0.5,0.2>', '<0.8,0.2>', '<0.5,0.5>', '<0.8,0.5>', '<1.0,0.5>', '<rand>'])

    df = pd.DataFrame(data[0:2,:], 
                 index=indexes[0:2],
                 columns=pd.Index(['tad', 'tas', 'tdd', 'tds', 'fd', 'fs', 'vd', 'vs', 'tid', 'tis', 'bd', 'bs', 'sd', 'ss'], 
                 name='Legend'))#.round(2)
    df.plot(kind='bar',figsize=(20,8), color=['darkblue', 'blue', 'darkgreen', 'lightgreen', 'darkred', 'red', 'darkcyan', 'cyan',
    'plum', 'violet', 'yellowgreen', 'yellow', 'teal', 'turquoise'])
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos,minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab,minor=True, rotation=90)
    ax.tick_params(axis='x', which='major', pad=30, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)

    plt.savefig(config+'_1.eps', format='eps')

    df = pd.DataFrame(data[2:4,:], 
                 index=indexes[2:4],
                 columns=pd.Index(['tad', 'tas', 'tdd', 'tds', 'fd', 'fs', 'vd', 'vs', 'tid', 'tis', 'bd', 'bs', 'sd', 'ss'], 
                 name='Legend'))#.round(2)
    df.plot(kind='bar',figsize=(20,8), color=['darkblue', 'blue', 'darkgreen', 'lightgreen', 'darkred', 'red', 'darkcyan', 'cyan',
    'plum', 'violet', 'yellowgreen', 'yellow', 'teal', 'turquoise'])
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos,minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab,minor=True, rotation=90)
    ax.tick_params(axis='x', which='major', pad=30, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)

    plt.savefig(config+'_2.eps', format='eps')

    df = pd.DataFrame(data[4:7,:], 
                 index=indexes[4:7],
                 columns=pd.Index(['tad', 'tas', 'tdd', 'tds', 'fd', 'fs', 'vd', 'vs', 'tid', 'tis', 'bd', 'bs', 'sd', 'ss'], 
                 name='Legend'))#.round(2)
    df.plot(kind='bar',figsize=(20,8), color=['darkblue', 'blue', 'darkgreen', 'lightgreen', 'darkred', 'red', 'darkcyan', 'cyan',
    'plum', 'violet', 'yellowgreen', 'yellow', 'teal', 'turquoise'])
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos,minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab,minor=True, rotation=90)
    ax.tick_params(axis='x', which='major', pad=30, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)

    plt.savefig(config+'_3.eps', format='eps')
    
    df = pd.DataFrame(data[7:8,:], 
                 index=indexes[7:8],
                 columns=pd.Index(['tad', 'tas', 'tdd', 'tds', 'fd', 'fs', 'vd', 'vs', 'tid', 'tis', 'bd', 'bs', 'sd', 'ss'], 
                 name='Legend'))#.round(2)
    df.plot(kind='bar',figsize=(20,8), color=['darkblue', 'blue', 'darkgreen', 'lightgreen', 'darkred', 'red', 'darkcyan', 'cyan',
    'plum', 'violet', 'yellowgreen', 'yellow', 'teal', 'turquoise'])
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x()+bar.get_width()/2.)

    ax.set_xticks(pos,minor=True)
    lab = []
    for i in range(len(pos)):
        l = df.columns.values[i//len(df.index.values)]
        lab.append(l)

    ax.set_xticklabels(lab,minor=True, rotation=90)
    ax.tick_params(axis='x', which='major', pad=30, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0)

    plt.savefig(config+'_4.eps', format='eps')

    '''
    ax = plt.subplot(111)
    ax.bar(x_pos-7*w-7*offset, dynamic_all, width=w, edgecolor='darkblue',align='center', fill=False)
    ax.bar(x_pos-6*w-6*offset, static_all, width=w, edgecolor='lightblue',align='center', fill=False, hatch='\\')

    
    ax.bar(x_pos-5*w-5*offset, dynamic_depend, width=w, edgecolor='darkgreen',align='center', fill=False)
    ax.bar(x_pos-4*w-4*offset, static_depend, width=w, edgecolor='lightgreen',align='center', fill=False, hatch='-')
    
    ax.bar(x_pos-3*w-3*offset, dynamic_fires, width=w, edgecolor='darkred', align='center', fill=False)
    ax.bar(x_pos-2*w-2*offset, static_fires, width=w, edgecolor='red', align='center', fill=False, hatch='/')
    
    ax.bar(x_pos-w-offset, dynamic_victims, width=w, edgecolor='darkcyan',align='center', fill=False)
    ax.bar(x_pos, static_victims, width=w, edgecolor='cyan',align='center', fill=False, hatch='\\')
    
    ax.bar(x_pos+w+offset, dynamic_time, width=w, edgecolor='darkviolet',align='center', fill=False)
    ax.bar(x_pos+2*w+2*offset, static_time, width=w, edgecolor='violet',align='center', fill=False, hatch='-')
    
    ax.bar(x_pos+3*w+3*offset, dynamic_base, width=w, edgecolor='darkturquoise',align='center', fill=False)
    ax.bar(x_pos+4*w+4*offset, static_base, width=w, edgecolor='turquoise',align='center', fill=False, hatch='/')

    ax.bar(x_pos+5*w+5*offset, dynamic_score, width=w, edgecolor='darkmagenta',align='center', fill=False)
    ax.bar(x_pos+6*w+6*offset, static_score, width=w, edgecolor='magenta',align='center', fill=False, hatch='\\')

    plt.xticks(x_pos, objects)
    plt.xticks(rotation=15) 
    plt.grid()
    '''
    #ax.autoscale(tight=True)
    plt.show()

def bar_plot_single_metric(fnames, config):
    temp = []
    with open(fnames[0], 'r') as f:
        lines = f.readlines()
        for line in lines:
            #print line
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
    for x in temp:
        print x
    # current order
    # 0         1           2       3           4       5           6       7
    # 1.0,0.0 - 0.5,0.0 - 1.0,0.5 - 0.5,0.5 - 0.8,0.2 - 0.5,0.2 - 0.8,0.5 - rand
    # order according to increasing gamma, then delta
    # 0.5,0.0 - 1.0,0.0 - 0.5,0.2 - 0.8,0.2 - 0.5,0.5 - 0.8,0.5 - 1.0,0.5 - rand
    dynamic_score = np.array([float(temp[1][1]), float(temp[0][1]), float(temp[5][1]), float(temp[4][1]), 
    float(temp[3][1]), float(temp[6][1]), float(temp[2][1]), float(temp[7][1])])
    print dynamic_score

    temp = []
    with open(fnames[1], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
            print line
            print len(line)

    dynamic_all = np.array( [ float(temp[1][3]), float(temp[0][3]), float(temp[5][3]), float(temp[4][3]), 
    float(temp[3][3]), float(temp[6][3]), float(temp[2][3]), float(temp[7][3]) ] )

    dynamic_depend = np.array( [ float(temp[1][6]), float(temp[0][6]), float(temp[5][6]), float(temp[4][6]), 
    float(temp[3][6]), float(temp[6][6]), float(temp[2][6]), float(temp[7][6]) ] )

    dynamic_fires = np.array( [ float(temp[1][7]), float(temp[0][7]), float(temp[5][7]), float(temp[4][7]), 
    float(temp[3][7]), float(temp[6][7]), float(temp[2][7]), float(temp[7][7]) ] )

    dynamic_victims = np.array( [ float(temp[1][8]), float(temp[0][8]), float(temp[5][8]), float(temp[4][8]), 
    float(temp[3][8]), float(temp[6][8]), float(temp[2][8]), float(temp[7][8]) ] )

    dynamic_time = np.array( [ float(temp[9][7]), float(temp[8][7]), float(temp[13][7]), float(temp[12][7]), 
    float(temp[11][7]), float(temp[14][7]), float(temp[10][7]), float(temp[15][7]) ] )

    dynamic_base = np.array( [ float(temp[9][8]), float(temp[8][8]), float(temp[13][8]), float(temp[12][8]), 
    float(temp[11][8]), float(temp[14][8]), float(temp[10][8]), float(temp[15][8]) ] )

    temp = []
    with open(fnames[2], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)
    # order according to increasing gamma, then delta
    # 0.5,0.0 - 1.0,0.0 - 0.5,0.2 - 0.8,0.2 - 0.5,0.5 - 0.8,0.5 - 1.0,0.5 - rand
    static_score = np.array([float(temp[1][1]), float(temp[0][1]), float(temp[5][1]), float(temp[4][1]), 
    float(temp[3][1]), float(temp[6][1]), float(temp[2][1]), float(temp[7][1])])
    print static_score

    temp = []
    with open(fnames[3], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub('[\\\$&lrangledymic]', '', line)
            line = filter(None, line.strip().split(' '))
            temp.append(line)

    static_all = np.array( [ float(temp[1][3]), float(temp[0][3]), float(temp[5][3]), float(temp[4][3]), 
    float(temp[3][3]), float(temp[6][3]), float(temp[2][3]), float(temp[7][3]) ] )

    static_depend = np.array( [ float(temp[1][6]), float(temp[0][6]), float(temp[5][6]), float(temp[4][6]), 
    float(temp[3][6]), float(temp[6][6]), float(temp[2][6]), float(temp[7][6]) ] )

    static_fires = np.array( [ float(temp[1][7]), float(temp[0][7]), float(temp[5][7]), float(temp[4][7]), 
    float(temp[3][7]), float(temp[6][7]), float(temp[2][7]), float(temp[7][7]) ] )

    static_victims = np.array( [ float(temp[1][8]), float(temp[0][8]), float(temp[5][8]), float(temp[4][8]), 
    float(temp[3][8]), float(temp[6][8]), float(temp[2][8]), float(temp[7][8]) ] )

    static_time = np.array( [ float(temp[9][7]), float(temp[8][7]), float(temp[13][7]), float(temp[12][7]), 
    float(temp[11][7]), float(temp[14][7]), float(temp[10][7]), float(temp[15][7]) ] )

    static_base = np.array( [ float(temp[9][8]), float(temp[8][8]), float(temp[13][8]), float(temp[12][8]), 
    float(temp[11][8]), float(temp[14][8]), float(temp[10][8]), float(temp[15][8]) ] )

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    ticks = ['<0.5,0.0>', '<1.0,0.0>', '<0.5,0.2>', '<0.8,0.2>', '<0.5,0.5>', '<0.8,0.5>', '<1.0,0.5>', '<rand>']
    #objects = ('all', 'depend', '<fires>', '<victims>', '<time>', '<base>', '<score>')
## ALL
    plt.figure()
    data_dynamic = [[dynamic_all[0]], [dynamic_all[1]], [dynamic_all[2]], [dynamic_all[3]], [dynamic_all[4]], [dynamic_all[5]],
    [dynamic_all[6]], [dynamic_all[7]]]

    data_static = [[static_all[0]], [static_all[1]], [static_all[2]], [static_all[3]], [static_all[4]], [static_all[5]], 
    [static_all[6]], [static_all[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)

    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of all completed tasks")

    plt.savefig(config+'_all.eps', format='eps')

## DEPEND
    plt.figure()
    data_dynamic = [[dynamic_depend[0]], [dynamic_depend[1]], [dynamic_depend[2]], [dynamic_depend[3]], [dynamic_depend[4]], [dynamic_depend[5]],
    [dynamic_depend[6]], [dynamic_depend[7]]]

    data_static = [[static_depend[0]], [static_depend[1]], [static_depend[2]], [static_depend[3]], [static_depend[4]], [static_depend[5]], 
    [static_depend[6]], [static_depend[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)

    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of dependent completed tasks")

    plt.savefig(config+'_depend.eps', format='eps')

## FIRES
    plt.figure()
    data_dynamic = [[dynamic_fires[0]], [dynamic_fires[1]], [dynamic_fires[2]], [dynamic_fires[3]], [dynamic_fires[4]], [dynamic_fires[5]],
    [dynamic_fires[6]], [dynamic_fires[7]]]

    data_static = [[static_fires[0]], [static_fires[1]], [static_fires[2]], [static_fires[3]], [static_fires[4]], [static_fires[5]], 
    [static_fires[6]], [static_fires[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of fires extinguished")

    plt.savefig(config+'_fires.eps', format='eps')

## VICTIMS
    plt.figure()
    data_dynamic = [[dynamic_victims[0]], [dynamic_victims[1]], [dynamic_victims[2]], [dynamic_victims[3]], [dynamic_victims[4]], [dynamic_victims[5]],
    [dynamic_victims[6]], [dynamic_victims[7]]]

    data_static = [[static_victims[0]], [static_victims[1]], [static_victims[2]], [static_victims[3]], [static_victims[4]], [static_victims[5]], 
    [static_victims[6]], [static_victims[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of victims saved")

    plt.savefig(config+'_victims.eps', format='eps')

## TIME
    plt.figure()
    data_dynamic = [[dynamic_time[0]], [dynamic_time[1]], [dynamic_time[2]], [dynamic_time[3]], [dynamic_time[4]], [dynamic_time[5]],
    [dynamic_time[6]], [dynamic_time[7]]]

    data_static = [[static_time[0]], [static_time[1]], [static_time[2]], [static_time[3]], [static_time[4]], [static_time[5]], 
    [static_time[6]], [static_time[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of time taken wrt timeout")

    plt.savefig(config+'_time.eps', format='eps')

## BASE
    plt.figure()
    data_dynamic = [[dynamic_base[0]], [dynamic_base[1]], [dynamic_base[2]], [dynamic_base[3]], [dynamic_base[4]], [dynamic_base[5]],
    [dynamic_base[6]], [dynamic_base[7]]]

    data_static = [[static_base[0]], [static_base[1]], [static_base[2]], [static_base[3]], [static_base[4]], [static_base[5]], 
    [static_base[6]], [static_base[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Percentage of times back to base vs. completed tasks")

    plt.savefig(config+'_base.eps', format='eps')

## SCORE
    plt.figure()
    data_dynamic = [[dynamic_score[0]], [dynamic_score[1]], [dynamic_score[2]], [dynamic_score[3]], [dynamic_score[4]], [dynamic_score[5]],
    [dynamic_score[6]], [dynamic_score[7]]]

    data_static = [[static_score[0]], [static_score[1]], [static_score[2]], [static_score[3]], [static_score[4]], [static_score[5]], 
    [static_score[6]], [static_score[7]]]

    bpl = plt.boxplot(data_dynamic, positions=np.array(xrange(len(data_dynamic)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data_static, positions=np.array(xrange(len(data_static)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpl, 'green') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, 'blue')

# draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='green', label='Dynamic')
    plt.plot([], c='blue', label='Static')
    plt.legend(loc="bottom right")

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks,rotation=15)
    plt.ylim(-0.1, 1.1)
    plt.xlim(-1.0, 16.0)
    plt.grid()
    plt.title("Overall score")

    plt.savefig(config+'_score.eps', format='eps')


if __name__ == '__main__':
    if not len(sys.argv) == 6:
        print 'Usage: ./plot_2.py config dynamicScore dynamic1 staticScore static1'
        sys.exit()

    name_of_files = []
    for x in range(2, len(sys.argv)):
        name_of_files.append(sys.argv[x])
        #print sys.argv[x]

    print name_of_files   
    bar_plot_single_metric(name_of_files, sys.argv[1])