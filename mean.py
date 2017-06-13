#!/usr/bin/env python

import sys
from numpy import *
import matplotlib.pyplot as plt;
plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np

import colormaps as cmaps

def create_heatmap(data, case):

    print data
    x = np.array(data[:,1])
    y = np.array(data[:,0])
    all = np.array(data[:,2])
    depend = np.array(data[:,3])

    xint = np.array([0,1,2,0,1,2,0,1,2])
    yint = np.array([0,0,0,1,1,1,2,2,2])

    grid_all = np.zeros((len(all)/3, 3))
    grid_all[xint,yint] = all

    grid_dep = np.zeros((len(depend)/3, 3))
    grid_dep[xint,yint] = depend

    print grid_all
    print grid_dep

    temp = np.array([0.0, 0.5, 1.0, 1.5])
    x, y = np.meshgrid(temp, temp)

    fig = plt.figure()
    plt.register_cmap(name='viridis', cmap=cmaps.viridis)
    plt.set_cmap(cmaps.viridis)
    plt.pcolormesh(x, y, grid_all, vmin=0., vmax=1.)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.title('All')
    fig.savefig('all_'+case+'.jpg')

    fig = plt.figure()
    plt.pcolormesh(x, y, grid_dep, vmin=0., vmax=1.)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.title('Depend')
    fig.savefig('depend_'+case+'.jpg')


def create_ave_matrix(fnames):
    tots = []
    for name in fnames:
        tots.append([])
        with open(name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                tots[len(tots) - 1].append(map(float, filter(None, line.strip().split(' '))))

    tots = np.array(tots)
    print tots
    halfs = tots[:,:,2:4]
    print halfs

    m = np.mean(halfs, axis=0)
    print m

    final_mean = np.zeros((9,4))
    final_mean[:,0:2] = tots[0,:,0:2]
    final_mean[:,2:4] = m

    return final_mean


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ./mean.py case file1 file2 ... fileN'
        sys.exit()

    case = sys.argv[1]
    name_of_files = []
    for x in range(2, len(sys.argv)):
        name_of_files.append(sys.argv[x])

    mean_vals = create_ave_matrix(name_of_files)
    create_heatmap(mean_vals, case)
