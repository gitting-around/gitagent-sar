#!/usr/bin/env python

import sys
from numpy import *
import matplotlib.pyplot as plt;
plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('/home/mfi01/catkin_ws/src/gitagent/result_scripts')
import colormaps as cmaps

def create_heatmap(dynamic, fname):
    data = []
    with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(map(float, filter(None, line.strip().split(' '))))

    data = np.array(data)
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
    fig.savefig(dynamic+'all_heatmap.jpg')

    fig = plt.figure()
    plt.pcolormesh(x, y, grid_dep, vmin=0., vmax=1.)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.title('Depend')
    fig.savefig(dynamic+'depend_heatmap.jpg')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ./plot_2.py static/dynamic tots_file'
        sys.exit()

    create_heatmap(sys.argv[1], sys.argv[2])


