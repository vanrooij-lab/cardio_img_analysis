#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:53:10 2022

@author: m.wehrens
"""


# Saved a version of the data generated in this script to:
# 20230116_backup-contrcorr-data-siRNAdes.spydata



# Let's try to in a very simple way process the beating heart cell images

import matplotlib as matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#import cv2
import numpy as np

import scipy.stats as stats

import scipy.signal as signal

import os

import pandas as pd

import cv2 # installed using terminal and pip; "pip install opencv-python"

from datetime import datetime # only for convenience purposes

import re

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)

import pickle

# Custom functions
import sys
sys.path.append("/Users/m.wehrens/Documents/git_repos/cardio_img_analysis/functions/")
from custom_functions_contractility import *
from custom_functions_movies import *

###############################################################################

# Load previously analyzed data:

# Note that using the standard save option from Spyder ("spydata" format) fails
# to load the file because of pickle issue.
# https://stackoverflow.com/questions/55890813/how-to-fix-object-arrays-cannot-be-loaded-when-allow-pickle-false-for-imdb-loa

# I'm going to do manual pickle at the end.
# Use the following line to load previous analysis:
    
# list_traces_corrcontr = pickle.load( open( my_work_dir+"saved_data/"+"2023-04-03"+"_list_traces_corrcontr.p", "rb" ) )

###############################################################################

"""
def readimg_roi(path, roi):
    img = mpimg.imread(path)[:,:,0]
    roi_img = img[roi[0]:roi[1],roi[2]:roi[3]]
    
    return roi_img
"""

###############################################################################

IMGNAMESUFFIX='_ch00'

my_work_dir = '/Volumes/Wehrens_Mic/RAW_DATA/2023-10-11/TIF_ORGANIZED/'

# For plate 2
my_out_dir   = '/Volumes/Wehrens_Mic/RAW_DATA/2023-10-11_Analysis/Analysis_Plate2/'
sample_annotation_filepath = my_out_dir+'2023_10_11_Tim_Ale__positions_CM.xlsx'

# For plate 1
my_out_dir   = '/Volumes/Wehrens_Mic/RAW_DATA/2023-10-11_Analysis/Analysis_Plate1/'
sample_annotation_filepath = my_out_dir+'2023_10_11_Tim_Ale__positions_CM_PLATE1.xlsx'


if not (os.path.isdir(my_out_dir)): 
    os.mkdir(my_out_dir)

###############################################################################
# This loads the sample meta data from the excel file
# You might need to execute this sectino multiple times to "refresh" the
# parameters when you update them in the excel.

def read_sample_information(sample_annotation_filepath):
    
    # Sample information
    # Assuming each of the samples correspond to a subdir of work dir defined above
    sample_info  = pd.read_excel(sample_annotation_filepath)
    
    # Sample list
    my_samples = sample_info['sample_name'].to_numpy()
    
    # Load more information
    
    # Dict with times between frames
    sample_info['dt'] = sample_info['duration_movie']/sample_info['total_frames']
    
    sample_dt = {sample_info['sample_name'][ii]:sample_info['dt'][ii] for ii in range(len(sample_info))}
    # ROIs for each of the movies
    sample_roi_ = {sample_info['sample_name'][ii]:sample_info['roi'][ii] for ii in range(len(sample_info))} # read ROI as string
    sample_roi  = {key:[int(x) for x in sample_roi_[key].replace('\ufeff','').split(', ')] for key in sample_roi_.keys()} # convert strings to int
    # Reference image for each of the movies (correlation will be determined between this one and all other ones)
    sample_refimg = {sample_info['sample_name'][ii]:sample_info['ref_frame'][ii] for ii in range(len(sample_info))}
    
    sample_info_dicts = {'dt':sample_dt,
                         'roi':sample_roi,
                         'refimg':sample_refimg,
                         'name':my_samples}
    
    return sample_info, sample_info_dicts
 

sample_info, sample_info_dicts =\
    read_sample_information(sample_annotation_filepath)
   
    

###############################################################################
# Create a series of movies, using custom scripted function loaded above
# Note that I only look at first 500 frames, skipping 10 frames, because
# it's too much data otherwise, and suits purposes.

movies_out_dir=my_out_dir+'movies_python_auto/'

if not (os.path.isdir(movies_out_dir)): 
    os.mkdir(movies_out_dir)

for current_sample_name in sample_info['sample_name'][sample_info['create_movie']=='yes']:

    # current_sample_name = sample_info['sample_name'][sample_info['create_movie']=='yes'].iloc[0]

    print('Creating movie for: '+current_sample_name)    
    
    image_dir=my_work_dir+current_sample_name+'/'
    image_filename_list = [current_sample_name+'_t'+str(idx).zfill(4)+'_ch00.tif' for idx in range(0,501,10)]
        
    current_dt=sample_info['dt'][sample_info['sample_name']==current_sample_name].values[0]
    fps_10skip=1/(current_dt*10)
    create_movie(image_filename_list, image_dir, movies_out_dir+current_sample_name, fps_10skip)


###############################################################################

S_IDX = 1 # sample index

###############################################################################
# Determine a region for this image set
# Put this in the excel file, and then reload informatino from the excel 
# file again

# Only determine ROI for user-selected samples, since some samples
# might be from the same position, so we want to later customize
# ROIs such that they are consistent between those positions.
# SELECTED_SAMPLES = ['2023_03_29.lif_A1-p1-nt', '2023_03_29.lif_A1-p2-nt', '2023_03_29.lif_A2-p1-nt', '2023_03_29.lif_A2-p2-nt', '2023_03_29.lif_B1-p1-nt', '2023_03_29.lif_B1-p2-nt', '2023_03_29.lif_B2-p1-nt', '2023_03_29.lif_B2-p2-nt']
SELECTED_SAMPLES = sample_info['sample_name'][sample_info['create_movie']=='yes'].values

def define_ROIs(my_work_dir, SELECTED_SAMPLES, IMGNAMESUFFIX = '_ch00'):
    
    #collected_ROIs = np.full([len(my_samples),4], np.nan)
    collected_ROIs = {}
    for current_sample in SELECTED_SAMPLES:
        
        print('Now showing '+current_sample)
        
        # Load the image
        img_idx=0
        img = mpimg.imread(my_work_dir+current_sample+'/'+current_sample+'_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'.tif')
        # img = img[:,:,0] # depends how images where exported
        img_norm = (img-np.min(img))/(np.max(img)-np.min(img))
        
        # Select the ROI
        roi_=cv2.selectROI('ROI_select', img_norm)
        roi = [roi_[1],  roi_[3]+roi_[1], roi_[0], roi_[2]+roi_[0]]
            # roi_ = x1, y1, dx, dy; but x and y reversal somewhere
            # roi = [y1,y2,x1,x2]
        
        cv2.destroyWindow('ROI_select') 
        cv2.waitKey(1) # required due to buggy cv2/gtk behavior https://stackoverflow.com/questions/6116564/destroywindow-does-not-close-window-on-mac-using-python-and-opencv
        
        imgplot = plt.imshow(img_norm[roi[0]:roi[1],roi[2]:roi[3]])
        plt.show()
        
        roi
        
        collected_ROIs[current_sample] = roi
        
        plt.close()
    
    return collected_ROIs

collected_ROIs = define_ROIs(my_work_dir, SELECTED_SAMPLES, IMGNAMESUFFIX)
collected_ROIs

df_ROI = \
    pd.DataFrame({
                    'Sample name':collected_ROIs.keys(),
                    'ROI':[str(v).replace('[','').replace(']','') for v in collected_ROIs.values()]  })
df_ROI.to_excel(my_out_dir+'automatic_ROIs.xlsx')

# Now add the above values into the annotation excel file, and reload the excel file 
# information using the line below.
sample_info, sample_info_dicts = read_sample_information(sample_annotation_filepath)

###############################################################################
# Output all ROI regions as images

ROI_dir = my_out_dir+'ROIs/'
if not (os.path.isdir(ROI_dir)): 
    os.mkdir(ROI_dir)

img_idx = 0

# Output all ROIs for the images
for S_IDX in range(len(sample_info_dicts['name'])):
    
    # S_IDX=4
    
    # Load the image
    img = mpimg.imread(my_work_dir+sample_info_dicts['name'][S_IDX]+'/'+sample_info_dicts['name'][S_IDX]+\
                        '_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'.tif')
    # img = img[:,:,0] # depends how images where exported        
    img_norm = (img-np.min(img))/(np.max(img)-np.min(img))
    
    # What are the ROI coordinates?
    current_roi = sample_info_dicts['roi'][sample_info_dicts['name'][S_IDX]]
    
    # Plot it
    F = plt.figure()
    imgplot = plt.imshow(img_norm[current_roi[0]:current_roi[1],current_roi[2]:current_roi[3]], cmap = 'gray')    
    plt.title(sample_info_dicts['name'][S_IDX])
    # plt.show()    
    plt.savefig(ROI_dir+'ROI_'+sample_info_dicts['name'][S_IDX]+'.pdf')
    plt.close(F)
    
###############################################################################

# See the script:    
# time_ale_contractility_dataset2_2023-10-11_EXTENSIONS.py
# for additional custom plots.
        




###############################################################################
###############################################################################
# Create a folder with cropped images
# NOTE THAT THIS TAKES LONG!

from datetime import datetime # for some reason throws error otherwise ..

ZIPCROPPED = False
NR_FRAMES = 1500 # frames 1 .. NR_FRAMES will be considered for the analysis
    # I now did 500 but there are already 4 datasets where it's better to 
    # take 1000 frames; probably best to repeat this analysis with the max
    # amount of frames and just store that data. (In this case, max 'd be 2000.)

if not os.path.exists(my_work_dir+'data_cropped'):
    os.mkdir(my_work_dir+'data_cropped')

for S_IDX in range(len(sample_info_dicts['name'])):
# for S_IDX in [S_IDX for S_IDX in range(len(sample_info_dicts['name'])) if '27_' in sample_info_dicts['name'][S_IDX]]:    
    
    # In case there are some exception-cases, this allows easy manual updating
    # S_IDX = 18; NR_FRAMES = 1000 
    # S_IDX = 23; NR_FRAMES = 1000    
    # S_IDX = 30; NR_FRAMES = 1000
    # S_IDX = 24; NR_FRAMES = 1000    
    
    # For convenience, give user some information
    print("Working on sample " + sample_info_dicts['name'][S_IDX]+', '+\
          str(S_IDX+1)+'/'+str(len(sample_info_dicts['name'])))
    current_date_and_time = datetime.now()
    print(str(current_date_and_time))
    
    # Get parameters
    roi = sample_info_dicts['roi'][sample_info_dicts['name'][S_IDX]]
    
    # Image path base
    my_image_dir = my_work_dir+sample_info_dicts['name'][S_IDX]+'/'
    
    # Now loop over images and correlate image with original image
    # note that I aimed for a frame rate of ±40fps, so if it beats
    # every 10 secs, i need to analyze 400 images ..

    if not os.path.exists(my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'):
        os.mkdir(my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/')
        
    for img_idx in range(0, NR_FRAMES):
        my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX  
        imgageXXXX_path = my_image_dir+my_img_filename+'.tif'
        img_XXXX = mpimg.imread(imgageXXXX_path)
                
        #np.save(my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'+sample_info_dicts['name'][S_IDX]+'_cropped.npy',\
        #             img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
        if ZIPCROPPED:
            np.savez_compressed(my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'+   my_img_filename+'_cropped.npz'    ,\
                                img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
        else:
            np.save(my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'+   my_img_filename+'_cropped.npy'    ,\
                                img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
            
        if (img_idx%200==0):
            print(str(round(img_idx/NR_FRAMES*100,1))+'% done..')
            

    
###############################################################################
###############################################################################
# Calculate the correlation using the a given frame as reference
# These reference frames will need to be calibrated, so this procedure might
# need to be iterated; therefor this will output each of the plots, and you
# should update the reference frames in the excel file. then, reload the excel 
# file, and repeat the procedure, until all reference frames are appropriate.

PREANA_dir = my_out_dir+'pre-analysis/'
if not (os.path.isdir(PREANA_dir)): 
    os.mkdir(PREANA_dir)

# S_IDX=0
# REF_IMG = 85
NR_FRAMES = 250

sample_info_dicts['name']

for S_IDX in range(len(sample_info_dicts['name'])):
# for S_IDX in [S_IDX for S_IDX in range(len(sample_info_dicts['name'])) if '27_' in sample_info_dicts['name'][S_IDX]]:
    
    # S_IDX=21; NR_FRAMES = 250
    
    print('Performing calculation for '+str(S_IDX+1)+'/'+str(len(sample_info_dicts['name'])))
    
    REF_IMG = sample_info_dicts['refimg'][sample_info_dicts['name'][S_IDX]]
    roi = sample_info_dicts['roi'][sample_info_dicts['name'][S_IDX]]    
    
    # Example of correlation calculation
    # thecorr, p = stats.pearsonr([1,2,3],[1,2,2])
    
    # my_image_base = my_work_dir+sample_info_dicts['name'][S_IDX]+'/'+sample_info_dicts['name'][S_IDX]+'_t'
    
    # Now loop over images and correlate image with original image
    # note that framerate is ±100 fps, if it beats every <4 seconds, 
    # i need to analysze 400 images ..
    # Load ref image from full path
    # refimage_path = my_image_base+str(REF_IMG).zfill(4)+IMGNAMESUFFIX+'.tif'
    # img_ref = mpimg.imread(refimage_path)
    
    # Load ref image from cropped version
    cropped_pic_dir = my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'
    my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(REF_IMG).zfill(4)+IMGNAMESUFFIX+'_cropped.npy'
    img_ref = np.load(cropped_pic_dir +  my_img_filename)         
            
    mytrace=[]
    for img_idx in range(0, NR_FRAMES):
        
        # Load the images (load from uncropped)
        # imgageXXXX_path = my_image_base+str(img_idx).zfill(4)+IMGNAMESUFFIX+'.tif'
        # img_XXXX = mpimg.imread(imgageXXXX_path)
        
        # Load images (load from already cropped files)
        cropped_pic_dir = my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'
        my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'_cropped.npy'
        img_XXXX = np.load(cropped_pic_dir +  my_img_filename)         
            
        # Calculate correlation        
        R,p=stats.pearsonr(img_ref.flatten(),  img_XXXX.flatten())
        mytrace.append(R)
        if (img_idx%10==0):
            print(str(round(img_idx/NR_FRAMES*100,2))+'% done..')
    
    # Simple plot w/ frame nrs & grid
    ###    
    
    f=np.array(range(0,NR_FRAMES))
    mytrace_1min = np.array([1-val for val in mytrace])
    fig, ax = plt.subplots()
    ax.plot(f,mytrace_1min)
    ax.plot(REF_IMG,0,'^k') # ###    
    plt.title(sample_info_dicts['name'][S_IDX])
    ax.set_xticks(np.arange(0,NR_FRAMES,50))
    ax.set_xticks(np.arange(0,NR_FRAMES,10), minor=True)
    ax.grid(axis = 'x', which='minor')
    ax.grid(axis = 'x', which='major')
    
    
    plt.savefig(PREANA_dir+'correlation_function_calibration_'+sample_info_dicts['name'][S_IDX]+'.pdf')
    # plt.show()
    plt.close(fig)
  

# Now put this information in the excel file, re-load the excel file with the
# code at the beginning, and execute this section again to make sure all plots
# look good.
sample_info, sample_info_dicts =\
    read_sample_information(sample_annotation_filepath)



###############################################################################
###############################################################################
# Contractility-plot based on correlation again
# Same as above, but now goes over full length
# of the movie. 
# NOTE THAT THIS TAKES LONG!

from datetime import datetime # for some reason throws error otherwise ..

NR_FRAMES = 1500 # frames 1 .. NR_FRAMES will be considered for the analysis
    # I now did 500 but there are already 4 datasets where it's better to 
    # take 1000 frames; probably best to repeat this analysis with the max
    # amount of frames and just store that data. (In this case, max 'd be 2000.)

list_traces_corrcontr = {}
for S_IDX in range(len(sample_info_dicts['name'])):
# for S_IDX in [S_IDX for S_IDX in range(len(my_samples)) if '27_' in my_samples[S_IDX]]:    
    
    # In case there are some exception-cases, this allows easy manual updating
    # S_IDX = 18; NR_FRAMES = 1000 
    # S_IDX = 23; NR_FRAMES = 1000    
    # S_IDX = 30; NR_FRAMES = 1000
    # S_IDX = 24; NR_FRAMES = 1000    
    
    # For convenience, give user some information
    print("Working on sample " + sample_info_dicts['name'][S_IDX]+', '+\
          str(S_IDX+1)+'/'+str(len(sample_info_dicts['name'])))
    current_date_and_time = datetime.now()
    print(str(current_date_and_time))
    
    # Get parameters
    REF_IMG = sample_info_dicts['refimg'][sample_info_dicts['name'][S_IDX]]
    # roi = sample_roi[my_samples[S_IDX]]
    
    # Example of correlation calculation
    # thecorr, p = stats.pearsonr([1,2,3],[1,2,2])
    
    # Image path base
    # my_image_base = my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'
    
    # Now loop over images and correlate image with original image
    # note that I aimed for a frame rate of ±40fps, so if it beats
    # every 10 secs, i need to analyze 400 images ..
    # refimage_path = my_image_base+str(REF_IMG).zfill(4)+IMGNAMESUFFIX+'.tif'
    # img_ref = mpimg.imread(refimage_path)
    # Load images (load from already cropped files)
    cropped_pic_dir = my_work_dir+'data_cropped/CROP_'+sample_info_dicts['name'][S_IDX]+'/'
    my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(REF_IMG).zfill(4)+IMGNAMESUFFIX+'_cropped.npy'
    img_ref = np.load(cropped_pic_dir +  my_img_filename)         
    
    mytrace=[]
    for img_idx in range(0, NR_FRAMES):
        
        # Load images (load from already cropped files)
        my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'_cropped.npy'
        img_XXXX = np.load(cropped_pic_dir +  my_img_filename)                 
        
        R,p=stats.pearsonr(img_ref.flatten(), img_XXXX.flatten())
        mytrace.append(R)
        if (img_idx%200==0):
            print(str(round(img_idx/NR_FRAMES*100,1))+'% done..')
            
    list_traces_corrcontr[sample_info_dicts['name'][S_IDX]] = mytrace
      
    

# Save important data
#    
# Explicitly save this parameter, to skip the lengthy part of the analysis
# later.
# Create output directory
if not os.path.exists(my_out_dir+"saved_data_py/"):
    os.mkdir(my_out_dir+"saved_data_py/")
# Create string with current date
current_date_and_time = datetime.now()
current_date = current_date_and_time.strftime("%Y-%m-%d")
# Save the parameter using pickle library
pickle.dump( list_traces_corrcontr, open( my_out_dir+"saved_data_py/"+current_date+"_list_traces_corrcontr.p", "wb" ) )
# To load, use
# list_traces_corrcontr = pickle.load( open( my_work_dir+"saved_data/"+"2023-04-03"+"_list_traces_corrcontr.p", "rb" ) )
    
###############################################################################
# Now post-process these signals (creates plots to double check what's done)

if not os.path.exists(my_out_dir+"analysis/"):
    os.mkdir(my_out_dir+"analysis/")

# Establish peaks and 1-signal
PEAKMINTIME   = .5 # estimate of minimum distance between peaks
SMOOTHINGTIME = .2 # estimate of minimum distance between peaks
PEAKMINHEIGHT = .8 # expressed as quantile
first_peaks = {}
second_peaks = {}
first_peak_height = {}
list_traces_1min = {}
list_minvals={}
list_maxvals={}

for S_IDX in range(len(sample_info_dicts['name'])):
    
    # S_IDX = 11
    
    current_trace      = list_traces_corrcontr[sample_info_dicts['name'][S_IDX]]    
    current_trace_1min = np.array([1-val for val in current_trace])

    f = np.arange(0,len(current_trace))
    
    # estimate time scale for peaks in terms of frames
    current_distance = int(round(PEAKMINTIME/sample_info_dicts['dt'][sample_info_dicts['name'][S_IDX]]))
    current_smoothing_window = int(round(SMOOTHINGTIME/sample_info_dicts['dt'][sample_info_dicts['name'][S_IDX]]))
    if (current_smoothing_window % 2 == 0):
        current_smoothing_window += 1
    
    # smooth data
    current_trace_1min_sav = signal.savgol_filter(current_trace_1min, current_smoothing_window, 3)
    
    # First identify the first peak in each one
    #req_height = np.max(current_trace_1min_sav)-.5*(np.max(current_trace_1min_sav)-np.min(current_trace_1min_sav))
    #
    #minval=np.quantile(current_trace_1min_sav, .01)
    #maxval=np.quantile(current_trace_1min_sav, .99)
    #req_height = .5*minval+.5*maxval
    req_height = np.quantile(current_trace_1min_sav, PEAKMINHEIGHT)
    peaks_in_mytrace_pos, _ = signal.find_peaks(current_trace_1min_sav, distance=current_distance, height=req_height)            
    
    # Take the 2nd peak as first peak, as sometimes the data starts within a peak
    # leading to artifacts
    current_firstpeak = peaks_in_mytrace_pos[1]
    current_second_peak = peaks_in_mytrace_pos[2]
    
    # collect results
    first_peaks[sample_info_dicts['name'][S_IDX]] = current_firstpeak
    second_peaks[sample_info_dicts['name'][S_IDX]] = current_second_peak    
    list_traces_1min[sample_info_dicts['name'][S_IDX]] = current_trace_1min
    list_minvals[sample_info_dicts['name'][S_IDX]]=np.quantile(current_trace_1min_sav, .02)
    list_maxvals[sample_info_dicts['name'][S_IDX]]=np.quantile(current_trace_1min_sav, .98)
    first_peak_height[sample_info_dicts['name'][S_IDX]]=current_trace_1min[current_firstpeak]
    
    # plot
    plt.plot(f, current_trace_1min)
    plt.plot(f,     current_trace_1min_sav, '--r')
    plt.plot(current_firstpeak, current_trace_1min[current_firstpeak],'ko')
    plt.plot(current_second_peak, current_trace_1min[current_second_peak],'ko')    
    plt.title('ID: '+sample_info_dicts['name'][S_IDX]+' ('+str(S_IDX)+')')
    #plt.ylim((0.06,0.09))
    
    plt.savefig(my_out_dir+'analysis/peakfinder_corr_'+sample_info_dicts['name'][S_IDX]+'_img.pdf')
    plt.show()

# Some debugging
if False:
    
    plt.hist(current_trace_1min_sav, color='lightgreen', ec='black', bins=15)
    np.quantile(current_trace_1min_sav, 1)
    np.quantile(current_trace_1min_sav, .8)      
    np.quantile(current_trace_1min_sav, .7)    
    np.quantile(current_trace_1min_sav, PEAKMINHEIGHT)

###############################################################################
# Create aligned plots, in two panels
# CURRENTLY NOT USED
# TO DO: UPDATE THIS PART

XMAX = 3.5

fig = plt.figure(figsize=(10/2.54,10/2.54), dpi=600) 

ax=fig.add_subplot(2, 1, 1)
samples_scrambled1hz = [sample for sample in my_samples if '-nt' in sample]
for sample_name in samples_scrambled1hz:
    
    current_trace          = list_traces_1min[sample_name]
    NR_FRAMES              = len(current_trace)    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'b-')
    #plt.plot(current_t_adj, current_trace,'b-')
    
plt.ylim((-.2,1.2))  
plt.xlim((-.5,XMAX))  # plt.xlim((-.5,1.5))  
plt.title('Untreated')
# Add grids
ax.set_xticks(np.arange(-.5,XMAX+.1,.5))
ax.set_xticks(np.arange(-.5,XMAX+.1,.1), minor=True)
ax.grid(axis = 'x', which='minor')
ax.grid(axis = 'x', which='major')

ax=fig.add_subplot(2, 1, 2)
SEARCHTERM = '0.3uM-EPI'
samples_siDes1hz = [sample for sample in my_samples if SEARCHTERM in sample]
for sample_name in samples_siDes1hz:
    
    current_trace          = list_traces_1min[sample_name]
    NR_FRAMES              = len(current_trace)       
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'r-')
    #plt.plot(current_t_adj, current_trace,'r-')

plt.ylim((-.2,1.2))
plt.xlim((-.5,XMAX))  # plt.xlim((-.5,1.5))  
plt.title(SEARCHTERM)
# Add grids
ax.set_xticks(np.arange(-.5,XMAX+.1,.5))
ax.set_xticks(np.arange(-.5,XMAX+.1,.1), minor=True)
ax.grid(axis = 'x', which='minor')
ax.grid(axis = 'x', which='major')

# Super labels x & y axes
ax=fig.add_subplot(1, 1, 1, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (s)')
plt.ylabel('1-corr (normalized)')
plt.tight_layout()


plt.show()


###############################################################################
# Multiple aligned plots, in two panels, but now also calculate some 
# parameters of interest

XMAX = 3.5

SEARCHTERMS = ['before_no-treatment$',     'after_no-treatment$', 
               'before_spiny-FB$',       'after_spiny-FB$', 'before_mus-FB$', 'after_mus-FB$', 
               'before_spiny-FB-medium$', 'after_spiny-FB-medium$', 'before_mus-FB-medium$',      'after_mus-FB-medium$']
mycolors    = ['b','r',
               'b','r','b','r',
               'b','r','b','r']

peak_durations_50 = {}

fig = plt.figure(figsize=(10/2.54,20/2.54), dpi=600) 

peak_durations={}
peak_durations_byterm={T:np.empty(0) for T in SEARCHTERMS} 
interpeak_times={}
interpeak_times_byterm={T:np.empty(0) for T in SEARCHTERMS}
first_peak_height_byterm = {T:np.empty(0) for T in SEARCHTERMS}
selected_samples_list_byterm = {}
for idx_t in range(len(SEARCHTERMS)):
    
    current_SEARCHTERM = SEARCHTERMS[idx_t]
    
    ax=fig.add_subplot(len(SEARCHTERMS), 1, idx_t+1)
    
    # selected_samples = [sample for sample in sample_info_dicts['name'] if current_SEARCHTERM in sample]
    # selected_samples = [sample for sample in sample_info_dicts['name'] if re.search(current_SEARCHTERM, sample)]   
    selected_samples = [sample_info_dicts['name'][idx] for idx in range(len(sample_info)) if re.search(current_SEARCHTERM, sample_info['condition'][idx])]    
    # Also store sample names per value
    selected_samples_list_byterm[current_SEARCHTERM] = selected_samples
        
    for sample_name in selected_samples:
        
        current_trace             = list_traces_1min[sample_name]        
        NR_FRAMES                 = len(current_trace)       
        current_firstpeak         = first_peaks[sample_name]
        current_second_peak       = second_peaks[sample_name]    
        current_first_peak_height = first_peak_height[sample_name]        
        current_firstpeak_time    = current_firstpeak*sample_info_dicts['dt'][sample_name]
        current_t                 = np.arange(0,NR_FRAMES)*sample_info_dicts['dt'][sample_name]
        current_t_adj             = current_t-current_firstpeak_time
        current_trace_norm        = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
        
        # Find the peak_duration_50
        interpeak_frames = current_second_peak - current_firstpeak
        peak2_regionstart_f  = current_second_peak - round(interpeak_frames/2)
        peak2_regionend_f    = current_second_peak + round(interpeak_frames/2)
        t_50a = location_closest_value(current_trace_norm[peak2_regionstart_f:current_second_peak], 0.5)+peak2_regionstart_f
        t_50b = location_closest_value(current_trace_norm[current_second_peak:peak2_regionend_f], 0.5)+current_second_peak    
        peak_duration_50 = t_50b-t_50a  
        # Collect the values
        peak_durations[sample_name] = peak_duration_50*sample_info_dicts['dt'][sample_name]
        peak_durations_byterm[current_SEARCHTERM] = np.append(peak_durations_byterm[current_SEARCHTERM],peak_duration_50*sample_info_dicts['dt'][sample_name])
        interpeak_times[sample_name] = interpeak_frames*sample_info_dicts['dt'][sample_name]
        interpeak_times_byterm[current_SEARCHTERM] = np.append(interpeak_times_byterm[current_SEARCHTERM],interpeak_frames*sample_info_dicts['dt'][sample_name])
        first_peak_height_byterm[current_SEARCHTERM] = np.append(first_peak_height_byterm[current_SEARCHTERM],current_first_peak_height)
        
        
        plt.plot(current_t_adj, current_trace_norm, mycolors[idx_t]+'-')
        plt.plot(0, current_trace_norm[current_firstpeak],'ko')
        plt.plot(current_t_adj[t_50a], 0.5, 'ko')
        plt.plot(current_t_adj[t_50b], 0.5, 'ko')    
        #plt.plot(current_t_adj, current_trace,'b-')
        
    plt.ylim((-.2,1.2))  
    plt.xlim((-.5,XMAX))  # plt.xlim((-.5,1.5))  
    plt.title(current_SEARCHTERM)
    # Add grids
    ax.set_xticks(np.arange(-.5,XMAX+.1,.5))
    ax.set_xticks(np.arange(-.5,XMAX+.1,.1), minor=True)
    ax.grid(axis = 'x', which='minor')
    ax.grid(axis = 'x', which='major')

# Super labels x & y axes
ax=fig.add_subplot(1, 1, 1, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (s)')
plt.ylabel('1-corr (normalized)')
plt.tight_layout()

plt.savefig(my_out_dir+'final_overview_traces.pdf', )
plt.show()

plt.close('all') 





# For now, I manually exported some of this data to Prism
peak_durations_byterm
interpeak_times_byterm
first_peak_height_byterm
selected_samples_list_byterm

# Export to excel
df_to_export = \
    pd.concat(
        [pd.DataFrame({
                    'peak_duration':peak_durations_byterm[SEARCHTERMS[idx]],
                    'interpeak':interpeak_times_byterm[SEARCHTERMS[idx]],
                    'peak_height':first_peak_height_byterm[SEARCHTERMS[idx]],
                    'condition_summarized':SEARCHTERMS[idx]},
                index=selected_samples_list_byterm[SEARCHTERMS[idx]]) for idx in range(len(SEARCHTERMS))]
        )
df_to_export.to_excel(my_out_dir+'final_overview_values.xlsx')


# Notes
# Striking that some numbers are precisely equal, e.g.:
# '2023-03-15-MW-PC-epi-titrate.lif_B2-p2-nt-r2': array([0.58004867]),
# '2023-03-15-MW-PC-epi-titrate.lif_B3-p2-nt-r2': array([0.58004867]),
# These are even from different wells -- note however that the 
# acquisition rate is 0.009831 s, so this simply means that 
# the length in terms of frames is 59 frames, and it seems reasonable that
# that value could be found exactly multiple times.













###############################################################################
###############################################################################
# Below some more stuff that was used previously, but not for my latest
# analysis.


###############################################################################
# Create aligned plots, on top of each other

NR_FRAMES = 500

fig = plt.figure(figsize=(7/2.54,7/2.54), dpi=600) 

ax=fig.add_subplot(1, 1, 1)
samples_scrambled1hz = [sample for sample in my_samples if '-nt' in sample]
for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'b-', linewidth=.5)
       
samples_siDes1hz = [sample for sample in my_samples if '10uM-EPI' in sample]
for sample_name in samples_siDes1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'r-' , linewidth=.5)

plt.ylim((-.2,1.2))
plt.xlim((-1,1)) 
ax.set_xticks(np.arange(-1,1+.1,.5))
ax.set_xticks(np.arange(-1,1+.1,.1), minor=True)
ax.grid(axis = 'x', which='minor', linewidth=.5)
ax.grid(axis = 'x', which='major', linewidth=.5)
plt.xlabel('Time (s)')
plt.ylabel('1-corr (normalized)')
    
plt.show()

###############################################################################
# Create aligned plots, now normalize plots

NR_FRAMES = 500

samples_scrambled1hz = [sample for sample in my_samples if '-nt' in sample]

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 
ax=fig.add_subplot(2, 1, 1)

for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    
    plt.plot(current_t_adj, current_trace)
    plt.plot(current_t_adj[current_firstpeak], current_trace[current_firstpeak],'ko')
    
plt.show()



NR_FRAMES = 500

samples_scrambled1hz = [sample for sample in my_samples if '10uM-EPI' in sample]

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 
ax=fig.add_subplot(2, 1, 1)

for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    
    plt.plot(current_t_adj, current_trace)
    plt.plot(current_t_adj[current_firstpeak], current_trace[current_firstpeak],'ko')
    
plt.show()

###############################################################################

# Now also find the peaks

mytrace_cut = np.array(mytrace)
mytrace_cut[mytrace_cut<(max(mytrace)*.9)]=0 
peaks_in_mytrace, _ = signal.find_peaks(mytrace_cut)
peak_times = sample_dt[my_samples[S_IDX]]*peaks_in_mytrace

###############################################################################

###############################################################################
# Now show the trace, showing peaks
# Also calculate inter-peak times

f=np.array(range(0,1000))
t=f*sample_dt[my_samples[S_IDX]]

mytrace_arr=np.array(mytrace)
plt.plot(t,mytrace)
plt.plot(t[peaks_in_mytrace],mytrace_arr[peaks_in_mytrace],'ro')
plt.xlabel('Time (s)')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")
plt.show()



###############################################################################
# Can we make a nice movie out of this?

# Set up some parameters
t=np.array(range(0,1000)) # TO DO: more convenient to do this at start

#######################
# Make plot 1
plt.plot(t,mytrace)
#plt.plot(t[10],mytrace[10],'ok') highlight a point
plt.xlabel('frame')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")
plt.show()

fig, (ax1, ax2) = plt.subplots(1,2)


#######################
# Plot with both trace and image

fig = plt.figure() # figsize=(10, 7)

fig.add_subplot(1, 2, 1)

plt.plot(t,mytrace)
plt.plot(t[10],mytrace[10],'ok')
plt.xlabel('frame')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")

fig.add_subplot(1, 2, 2)
plt.imshow(img[roi_c1:roi_c2,roi_r1:roi_r2])
plt.show()

fig.savefig(my_output_dir+'my_plot.tif')


#######################
# Plot with both trace and image


t_seconds=t*frame_interval

for img_idx in range(0,1000):
    
    # Load image
    imgageXXXX_path = my_image_dir+my_image_base+str(img_idx).zfill(4)+'.tif'
    img_XXXX = mpimg.imread(imgageXXXX_path)
    
    # Create the figure
    my_dpi=300 # (arbitrary, actually)
    fig = plt.figure(figsize=(1600/my_dpi, 800/my_dpi), dpi=my_dpi) # figsize=(10, 7)
    
    fig.add_subplot(1, 2, 1)
    
    plt.plot(t_seconds,mytrace)
    plt.plot(t_seconds[img_idx],mytrace[img_idx],'ok')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Correlation with image 0')
    plt.title("Trace v0")
    
    fig.add_subplot(1, 2, 2)
    plt.imshow(img_XXXX[roi_c1:roi_c2,roi_r1:roi_r2])
    plt.title('Image @ '+str(np.round(t_seconds[img_idx],2))+' seconds')
    
    fig.savefig(my_output_dir+'my_plot_'+str(img_idx)+'.tif')

    if (img_idx%25==0):
        print(str(img_idx/1000*100)+'% done..')
        plt.show()

    plt.close(fig)

###############################################################################


#####


# test code
img_0010 = mpimg.imread(my_image_dir+my_image_base+str(10).zfill(4)+'.tif')
stats.pearsonr(img_0000[roi_c1:roi_c2,roi_r1:roi_r2].flatten(), img_0010[roi_c1:roi_c2,roi_r1:roi_r2].flatten())

###############################################################################

#read image
img_raw = cv2.imread(my_image_path)

#select ROI function
roi = cv2.selectROI(img_raw)

#print rectangle points of selected roi
print(roi)

#Crop selected roi from raw image
roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

#show cropped image
cv2.imshow("ROI", roi_cropped)

cv2.imwrite("crop.jpeg",roi_cropped)

#hold window
cv2.waitKey(0)





