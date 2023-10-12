#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:59:38 2023

@author: m.wehrens
"""


import matplotlib.animation as animation

import numpy as np
from pylab import *

import matplotlib.pyplot as plt

import random



def rand(X,Y):
    return [[random.random() for x in range(0,X)] for y in range(0,Y)] 

def ani_frame():
    
    dpi = 100
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    im = ax.imshow(rand(300,300),cmap='gray',interpolation='nearest')
    im.set_clim([0,1])
    fig.set_size_inches([5,5])

    plt.tight_layout()


    def update_img(n): # will be called from FuncAnimation, 
        print(n)
        tmp = rand(300,300)
        im.set_data(tmp)
        return im

    #legend(loc=0)
    ani = animation.FuncAnimation(fig,func=update_img,frames=50,interval=30)
        # note that frames can be array that's passed, or simply # which will create range
    writer = animation.writers['ffmpeg'](fps=30)

    ani.save('/Volumes/Wehrens_Mic/RAW_DATA/test/demo.mp4',writer=writer,dpi=dpi)
    return ani

ani_frame()