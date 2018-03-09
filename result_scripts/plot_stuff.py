#!/usr/bin/env python
import sys
from numpy import *
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D

plt.rcdefaults()
import numpy as np
    
def gamma_delta(fnames):
    pieces = []
    for fname in fnames:
        with open(fname, 'r') as f:
            lines = f.readlines()
            pieces.append(filter(None, lines[6].strip().split(',')))

    i = 0
    colors = np.random.random((len(pieces), 3))
    circle_area = np.pi * (6 * np.random.rand(len(pieces)))**2
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    for y in pieces:
        points = []
        fig = plt.figure()
        for x in y:
            points.append(filter(None, x.split(' ')))
        # print points
        # Plot the points
        gamma = []
        delta = []
        for point in points:
            if point[0] == '0':
                delta.append(float(point[1]))
                gamma.append(float(point[6]))
            else:
                gamma.append(float(point[1]))
                delta.append(float(point[6]))
        #print circle_area[i]
        #print np.arange(len(delta))
        colors = np.random.random((len(points), 3))
        circle_area = np.pi * (15 * np.random.rand(len(points)))**2
        plt.scatter(gamma, delta, c=colors, s=circle_area, alpha=0.3)
        
        i += 1  
        
        axes = plt.gca()
        axes.set_xlim([-0.5,1.5])
        axes.set_ylim([-0.5,1.5])
        #ax.set_xlabel('Gamma')
        #ax.set_ylabel('Delta')
        plt.xlabel('Gamma')
        plt.ylabel('Delta')
    plt.show()


def gamma_delta_2(fnames):
    pieces = []
    for fname in fnames:
        with open(fname, 'r') as f:
            lines = f.readlines()
            pieces.append(filter(None, lines[6].strip().split(',')))

    i = 0
    colors = np.random.random((len(pieces), 3))
    circle_area = np.pi * (10 * np.random.rand(len(pieces)))**2
    
    gamma = []
    delta = []
    
    for y in pieces:
        gamma.append([])
        delta.append([])
        points = []
        for x in y:
            points.append(filter(None, x.split(' ')))
        # print points
        # Plot the points
        for point in points:
            if point[0] == '0':
                delta[-1].append(float(point[1]))
                gamma[-1].append(float(point[6]))
            else:
                gamma[-1].append(float(point[1]))
                delta[-1].append(float(point[6]))


    gamma = np.array(gamma)
    delta = np.array(delta)
    
    maxi_len = max([len(x) for x in gamma])
    print maxi_len
    i = 0
    while i < maxi_len:
        fig = plt.figure()
        for x in range(i, i+30):
            plt.subplot(5,6,x+1-i)
            for y in range(0, len(gamma)):
                
                if x < len(gamma[y]):
                    plt.scatter(gamma[y][x], delta[y][x], c=colors[y], s=circle_area[y], alpha=0.3)
                    axes = plt.gca()
                    axes.set_xlim([-0.5,1.5])
                    axes.set_ylim([-0.5,1.5])
                    plt.xlabel('Gamma')
                    plt.ylabel('Delta')
        fig.set_size_inches(20, 15, forward=True)
        fig.savefig(str(i) +'_gamma_delta_ag.jpg', dpi=200)
        i += 30

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ./get_last_lines.py gamma_deltas_file'
        sys.exit()        
        
    name_of_files = []
    for x in range(1, len(sys.argv)):
        name_of_files.append(sys.argv[x])
    gamma_delta_2(name_of_files)  
