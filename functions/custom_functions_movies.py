#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:21:49 2023

@author: m.wehrens
"""

import matplotlib.animation as animation

import numpy as np
from pylab import *

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import random


def create_movie(image_filename_list, image_dir, out_movie_path, my_fps):
    
    dpi = 300
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    image0 = mpimg.imread(image_dir+image_filename_list[0])
    im = ax.imshow(image0,cmap='gray',interpolation='nearest')
    im.set_clim([0,255])
    fig.set_size_inches([6,6])
    
    annot_txt = ax.text(25, 25, 'frame='+str(0), ha='left', va='top')

    def get_image(idx):
        the_image = mpimg.imread(image_dir+image_filename_list[idx])
        im.set_data(the_image)
        annot_txt.set_text('img='+image_filename_list[idx])
        if (idx % 10 == 0):
            print(str(round(100*idx/len(image_filename_list)))+'%')
        return im

    plt.tight_layout()

    #legend(loc=0)
    ani = animation.FuncAnimation(fig,get_image,range(1,len(image_filename_list)),interval=1000/my_fps)
    writer = animation.writers['ffmpeg'](fps=my_fps)

    ani.save(out_movie_path+'.mp4',writer=writer,dpi=dpi)
    
    plt.close(fig)
    return ani

# Some code to try above
if False:
    
    image_dir='/Volumes/Wehrens_Mic/RAW_DATA/2023-09-26/images/A4_p2/'
    image_filename_list = ['A4_p2_t'+str(idx).zfill(4)+'_ch00.tif' for idx in range(0,500,10)]
    
    create_movie(image_filename_list, image_dir, 94/10)


