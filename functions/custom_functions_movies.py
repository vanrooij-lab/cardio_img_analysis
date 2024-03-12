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

# import random

###############################################################################

def create_movie(image_filename_list, image_dir, out_movie_path, my_fps):
    
    dpi = 300
    
    # Set up figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Set up the first image
    image0 = mpimg.imread(image_dir+image_filename_list[0])
    im = ax.imshow(image0,cmap='gray',interpolation='nearest')
    im.set_clim([0,255])
    fig.set_size_inches([6,6])
    
    annot_txt = ax.text(25, 25, 'frame='+str(0), ha='left', va='top')

    # Function to update the image
    def get_image(idx):
        
        the_image = mpimg.imread(image_dir+image_filename_list[idx])
        im.set_data(the_image)
        annot_txt.set_text('img='+image_filename_list[idx])
        if (idx % 10 == 0):
            print(str(round(100*idx/len(image_filename_list)))+'%')

        return im

    plt.tight_layout()

    #legend(loc=0)
    ani = animation.FuncAnimation(fig, get_image, range(1,len(image_filename_list)), interval=1000/my_fps)
    # ani = animation.FuncAnimation(fig, get_image, range(1,20), interval=1000/my_fps)
    # ani = animation.FuncAnimation(fig, get_image, range(1,51), interval=1000/my_fps)
    # DEBUGGING
    #ani = animation.FuncAnimation(fig, get_image, range(1,10), interval=1000/my_fps)
    # ani = animation.FuncAnimation(fig, get_image, range(1,2))
    writer = animation.writers['ffmpeg'](fps=my_fps)

    ani.save(out_movie_path+'.mp4', writer=writer, dpi=dpi)
    
    plt.pause(1) # this prevents some very weird error to occur, involving a nonetype and add_callback error
    plt.close(fig)

    # return ani
    return None

###############################################################################


def create_movies(sample_info, my_work_dir, movies_out_dir, subsel=None):

    # Set subsel to a number if you only want to analyze a subset of samples
    if subsel is None:
        subsel = np.sum(sample_info['create_movie']=='yes')

    # Loop over samples, create movie
    for current_sample_name in sample_info['sample_name'][sample_info['create_movie']=='yes'].head(subsel):
        # Debugging
        # current_sample_name=sample_info['sample_name'][sample_info['create_movie']=='yes'].iloc[0]

        # Setting some parameters
        print('Creating movie for: '+current_sample_name)    
        image_dir=my_work_dir+current_sample_name+'/'
        image_filename_list = [current_sample_name+'_t'+str(idx).zfill(4)+'_ch00.tif' for idx in range(0,501,10)]
        current_dt=sample_info['dt'][sample_info['sample_name']==current_sample_name].values[0]
        fps_10skip=1/(current_dt*10)

        # Create the movie
        create_movie(image_filename_list, image_dir, out_movie_path = movies_out_dir+current_sample_name, my_fps = fps_10skip)


###############################################################################

# Some code to try above
if False:
    
    image_dir='/Volumes/Wehrens_Mic/RAW_DATA/2023-09-26/images/A4_p2/'
    image_filename_list = ['A4_p2_t'+str(idx).zfill(4)+'_ch00.tif' for idx in range(0,500,10)]
    
    create_movie(image_filename_list, image_dir, 94/10)


