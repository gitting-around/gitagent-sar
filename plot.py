#!/usr/bin/env python
import sys
from numpy import *
import math
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import random
import numpy as np
import time


def create_2D_graph(lines, names, simName):
    fig = plt.figure()
    high = 0.7
    low = 0.3
    x = range(0, len(lines[0]))
    '''
    lowLine = np.array([low for i in xrange(len(x))])
    plt.plot(x, lowLine, 'y--', label='low')  # plotting low threshold
    highLine = np.array([high for i in xrange(len(x))])
    plt.plot(x, highLine, 'g--', label='high')  # plotting high threshold'''

    height = 1

    for index, l in enumerate(lines):
        k = np.array(l)
        plt.plot(x, k+index*height, label=names[index])  # plotting t,a separately
        print names[index]

    fig.suptitle('Relation', fontsize=20)
    plt.xlabel('steps', fontsize=18)
    name = ''
    for x in names:
        name += x + '_'
    plt.ylabel(name, fontsize=16)
    legend = plt.legend(loc='center right', shadow=True)
    fig.savefig(simName+'_'+name + '.jpg')
    #plt.show()


def create_bar_plot(ave, name):
    fig = plt.figure()

    objects = ('ta', 'tda', 'tc', 'tdc','sta', 'std', 'cn', 'req', 'req_s', 'req_r', 'req_r_a', 'req_acc')
    y_pos = np.arange(len(objects))
    performance = ave

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Value')
    plt.title('Preliminary')

    fig.savefig(name+'_tasks_TOT.jpg')
    #plt.show()


def create_grouped_bar_plot(ave, name):

    ta = ave[0:3]
    tda = ave[3:6]
    tc = ave[6:9]
    tdc = ave[9:12]
    sta = ave[12:15]
    stc = ave[15:18]
    requests = ave[21:24]
    requests_success = ave[24:27]
    requests_received = ave[27:30]
    requests_accept = ave[30:33]
    requests_acc_succ = ave[33:]

    req_ta = [requests[0]/float(ta[0])*100, requests[1]/float(ta[1])*100, requests[2]/float(ta[2])*100]

    reqRec_ta = [requests_received[0]/float(ta[0])*100, requests_received[1]/float(ta[1])*100, requests_received[2]/float(ta[2])*100]

    reqRec_tc = [requests_received[0]/float(tc[0])*100, requests_received[1]/float(tc[1])*100, requests_received[2]/float(tc[2])*100]

    # Plot tasks with respect to difficulty
    pos = list(range(len(ta)))
    width = 0.125 # 1/(6+2)

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10,10))

    # Create a bar with pre_score data,
    # in position pos,
    plt.bar(pos,
        #using df['pre_score'] data,
        tc,
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='bisque',
        # with label the first value in first_name
        label='tc')

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos], ta, width, alpha=0.5, color='powderblue', label='ta')
    plt.bar([p + width*2 for p in pos], tdc, width, alpha=0.5, color='palegreen', label='tdc')
    plt.bar([p + width*3 for p in pos], tda, width, alpha=0.5, color='linen', label='tda')
    plt.bar([p + width*4 for p in pos], stc, width, alpha=0.5, color='paleturquoise', label='stc')
    plt.bar([p + width*5 for p in pos], sta, width, alpha=0.5, color='lavenderblush', label='sta')

    # Set the y axis label
    ax.set_ylabel('Nr of Tasks')

    # Set the chart's title
    ax.set_title('Results')

    # Set the position of the x ticks
    ax.set_xticks([p + 3.5* width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(['easy', 'medium', 'hard'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*8)
    #plt.ylim([0, max(req+ta+tda++tc+tdc+tas+tcs+cn)] )

    # Adding the legend and showing the plot
    plt.legend(['tc', 'ta', 'tdc', 'tda', 'stc', 'sta'], loc='upper right')
    plt.grid()
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(name+'_tasks.jpeg', bbox_inches=extent.expanded(1.1, 1.2))

    ########################################################################################
    # Plot requests with respect to difficulty
    pos = list(range(len(requests)))
    width = 0.145 # 1/(5+2)

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10,10))

    # Create a bar with pre_score data,
    # in position pos,
    plt.bar(pos,requests,width,alpha=0.5,color='bisque',label='req')
    plt.bar([p + width for p in pos], requests_success, width, alpha=0.5, color='powderblue', label='req_s')
    plt.bar([p + width*2 for p in pos], requests_received, width, alpha=0.5, color='palegreen', label='req_rec')
    plt.bar([p + width*3 for p in pos], requests_accept, width, alpha=0.5, color='linen', label='req_rec_acc')
    plt.bar([p + width*4 for p in pos], requests_acc_succ, width, alpha=0.5, color='paleturquoise', label='req_rec_s')

    # Set the y axis label
    ax.set_ylabel('Nr of Requests')

    # Set the chart's title
    ax.set_title('Results')

    # Set the position of the x ticks
    ax.set_xticks([p + 3.5* width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(['easy', 'medium', 'hard'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*8)
    #plt.ylim([0, max(req+ta+tda++tc+tdc+tas+tcs+cn)] )

    # Adding the legend and showing the plot
    plt.legend(['req', 'req_s', 'req_rec', 'req_acc', 'req_rec_s'], loc='upper right')
    plt.grid()
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(name+'_requests.jpeg', bbox_inches=extent.expanded(1.1, 1.2))

    #########################################################
    fig, ax = plt.subplots(figsize=(10,10))
    pos = list(range(len(req_ta)))
    width = 0.2 #1.0 / (nr of ticks + 2)
    plt.bar(pos, req_ta, width, alpha=0.5, color='lavender', label='req_ta')
    plt.bar([p + width for p in pos], reqRec_ta, width, alpha=0.5, color='powderblue', label='reqRec_ta')
    plt.bar([p + width*2 for p in pos], reqRec_tc, width, alpha=0.5, color='palegreen', label='reqRec_tc')
    # Set the y axis label
    ax.set_ylabel(' Value (%)')

    # Set the chart's title
    ax.set_title('Request received and issued')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.0 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(['easy', 'medium', 'hard'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    #plt.ylim([0, max(req+ta+tda++tc+tdc+tas+tcs+cn)] )

    # Adding the legend and showing the plot
    plt.legend(['Requests issued', 'Requests received', 'Req received success'], loc='upper right')
    plt.grid()
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(name+'_percent.jpeg', bbox_inches=extent.expanded(1.1, 1.2))

    #plt.show()


def read_from_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
        # Theta
        factors = map(float, filter(None, lines[0].strip().split(' ')))
        print factors
        tasks = map(float, filter(None, lines[1].strip().split(' ')))
        print tasks
        theta = map(float, filter(None, lines[2].strip().split(' ')))
        print theta
        esteem = map(float, filter(None, lines[3].strip().split(' ')))
        print esteem
        tu = map(float, filter(None, lines[4].strip().split(' ')))
        print tu
        ti = map(float, filter(None, lines[5].strip().split(' ')))
        print ti
        culture = map(float, filter(None, lines[6].strip().split(' ')))
        print culture
        candido = map(float, filter(None, lines[7].strip().split(' ')))
        print candido
        deps = map(float, filter(None, lines[8].strip().split(' ')))
        print deps
        health = map(float, filter(None, lines[9].strip().split(' ')))
        print health
        theta_bool = map(float, filter(None, lines[10].strip().split(' ')))
        print theta_bool

        # Gamma
        gamma = map(float, filter(None, lines[11].strip().split(' ')))
        print gamma
        gamma_esteem = map(float, filter(None, lines[12].strip().split(' ')))
        print gamma_esteem
        gamma_bool = map(float, filter(None, lines[13].strip().split(' ')))
        print gamma_bool

        return factors, tasks, theta, esteem, tu, ti, culture, candido, deps, health, theta_bool, gamma, gamma_esteem, gamma_bool


def average(lista):
    lista = np.array(lista)
    return np.mean(lista, axis=0)


def total(lista):
    i = 0
    total = []
    while i < len(lista):
        total.append(sum([lista[i], lista[i+1], lista[i+2]]))
        i += 3
    return total


def subtract_noones(lista):
    lista[0:3] = lista[0:3] - lista[18:21]
    lista[3:6] = lista[3:6] - lista[18:21]
    lista[12:15] = lista[12:15] - lista[18:21]
    return lista

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: ./visualize_results.py name filename'
        sys.exit()
    params4file = []
    someparams = []
    name = sys.argv[1]
    for x in range(2, len(sys.argv)):
        fname = sys.argv[x]
        print fname
        factor_track, tasks, theta, esteem, tu, ti, culture, candido, deps, health, theta_bool, gamma, gamma_esteem, gamma_bool = read_from_file(fname)
        params4file.append((factor_track, tasks, theta, esteem, tu, ti, culture, candido, deps, health, theta_bool, gamma, gamma_esteem, gamma_bool))
        someparams.append(tasks)
        print '\n\n'

    someparams = np.array(someparams)
    print someparams

    for x in someparams:
        x = subtract_noones(x)

    ave = average(someparams)
    print ave

    create_grouped_bar_plot(ave, name)

    tots = total(ave)
    print tots
    create_bar_plot(tots, name)

    '''create_2D_graph([theta, theta_bool, esteem, tu, ti, culture, candido, deps, health],
                    ['theta', 'theta_bool', 'esteem', 'tu', 'ti', 'culture', 'candido', 'deps', 'health'])'''

    create_2D_graph([theta, theta_bool], ['theta', 'theta_bool'], name)
    create_2D_graph([theta, esteem], ['theta', 'theta_esteem'], name)
    create_2D_graph([theta, ti], ['theta', 'theta_ti'], name)
    create_2D_graph([theta, tu], ['theta', 'theta_tu'], name)
    create_2D_graph([theta, culture], ['theta', 'theta_culture'], name)
    create_2D_graph([theta, candido], ['theta', 'theta_candid'], name)
    create_2D_graph([theta, health], ['theta', 'theta_health'], name)

    create_2D_graph([theta, deps[0:][::2]], ['theta', 'abil'], name)
    create_2D_graph([theta, deps[1:][::2]], ['theta', 'res'], name)

    create_2D_graph([gamma_bool, gamma_esteem], ['gamma_bool', 'gamma_esteem'], name)






