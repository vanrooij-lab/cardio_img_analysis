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

my_work_dir = '/Volumes/Wehrens_Mic/IMG_ANALYSIS/2023_03_29_MW-EPI-r2/'

my_out_dir   = my_work_dir+'out/'

if not (os.path.isdir(my_out_dir)): 
    os.mkdir(my_out_dir)

###############################################################################
# This loads the sample meta data from the excel file
# You might need to execute this sectino multiple times to "refresh" the
# parameters when you update them in the excel.

# Sample information
# Assuming each of the samples correspond to a subdir of work dir defined above
sample_info  = pd.read_excel(my_work_dir+'2023-03-29_sample_metadata.xlsx')

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
 
###############################################################################

S_IDX = 1 # sample index

###############################################################################
# Load image and show it
# Just for convenience, this is not a necessary part of the script

#my_image_dir = '/Volumes/workdrive_m.wehrens_hubrecht/microscopy_images/pictures/'
#my_image = 'pilot-4nov_b1_pos1_movie_t0000.tif'
#my_image_base = 'pilot-4nov_b1_pos1_movie_t'
#my_image_path = my_image_dir+my_image

img_idx=0
# img_ = mpimg.imread(my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')
img_ = mpimg.imread(my_work_dir+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')

# Collapse the image from RGB to single grey value
img = img_[:,:,0]
# Sanity check
if (np.all(img_[:,:,0]==img_[:,:,1])):
    print("Check passed")
else:
    print("Check failed")

# normalize image
# note that the signal will vary from one image to the next
# so we don't want to normalize on single-image basis in the eventual analysis
img_norm = (img-np.min(img))/(np.max(img)-np.min(img))


imgplot = plt.imshow(img_norm, cmap = 'gray')
#imgplot = plt.imshow(img_norm, vmin = 0.4, vmax=.6)#, norm=colors.PowerNorm(gamma=1. / 2.))
plt.show()

###############################################################################
# Determine a region for this image set
# Put this in the excel file, and then reload informatino from the excel 
# file again

# Only determine ROI for use-selected samples, since some samples
# might be from the same position, so we want to later customize
# ROIs such that they are consistent between those positions.
SELECTED_SAMPLES = ['2023_03_29.lif_A1-p1-nt', '2023_03_29.lif_A1-p2-nt', '2023_03_29.lif_A2-p1-nt', '2023_03_29.lif_A2-p2-nt', '2023_03_29.lif_B1-p1-nt', '2023_03_29.lif_B1-p2-nt', '2023_03_29.lif_B2-p1-nt', '2023_03_29.lif_B2-p2-nt']

#collected_ROIs = np.full([len(my_samples),4], np.nan)
collected_ROIs = {}
for current_sample in SELECTED_SAMPLES:
    
    # Load the image
    img_idx=0
    img_ = mpimg.imread(my_work_dir+current_sample+'/'+current_sample+'_t'+str(img_idx).zfill(4)+'.tif')
    img = img_[:,:,0]
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

collected_ROIs

# Now go back to the section that updates the sample information from the excel
# file (don't forget to save the excel file)

###############################################################################
# Output all ROI regions as images

img_idx = 1

# Output all ROIs for the images
for S_IDX in range(len(my_samples)):
    
    img_ = mpimg.imread(my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')
    img_norm = (img-np.min(img))/(np.max(img)-np.min(img))
    
    current_roi = sample_roi[my_samples[S_IDX]]
    
    imgplot = plt.imshow(img_norm[current_roi[0]:current_roi[1],current_roi[2]:current_roi[3]], cmap = 'gray')
    
    plt.savefig(my_out_dir+'ROI_'+my_samples[S_IDX]+'.pdf')
    plt.show()
    
    
###############################################################################
###############################################################################
# Calculate the correlation using the a given frame as reference
# These reference frames will need to be calibrated, so this procedure might
# need to be iterated; therefor this will output each of the plots, and you
# should update the reference frames in the excel file. then, reload the excel 
# file, and repeat the procedure, until all reference frames are appropriate.

# S_IDX=0
# REF_IMG = 85
NR_FRAMES = 250

for S_IDX in range(len(my_samples)):
    
    # S_IDX=23; NR_FRAMES = 700
    
    print('Performing calculation for '+str(S_IDX+1)+'/'+str(len(my_samples)))
    
    REF_IMG = sample_refimg[my_samples[S_IDX]]
    roi = sample_roi[my_samples[S_IDX]]    
    
    # Example of correlation calculation
    # thecorr, p = stats.pearsonr([1,2,3],[1,2,2])
    
    my_image_base = my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'
    
    # Now loop over images and correlate image with original image
    # note that I aimed for a frame rate of ±40fps, so if it beats
    # every 10 secs, i need to analysze 400 images ..
    refimage_path = my_image_base+str(REF_IMG).zfill(4)+'.tif'
    img_ref = mpimg.imread(refimage_path)
    mytrace=[]
    for img_idx in range(0, NR_FRAMES):
        imgageXXXX_path = my_image_base+str(img_idx).zfill(4)+'.tif'
        img_XXXX = mpimg.imread(imgageXXXX_path)
        R,p=stats.pearsonr(img_ref[roi[0]:roi[1],roi[2]:roi[3]].flatten(),
                         img_XXXX[roi[0]:roi[1],roi[2]:roi[3]].flatten())
        mytrace.append(R)
        if (img_idx%10==0):
            print(str(img_idx/NR_FRAMES*100)+'% done..')
    
    # Simple plot w/ frame nrs & grid
    ###    
    
    f=np.array(range(0,NR_FRAMES))
    mytrace_1min = np.array([1-val for val in mytrace])
    fig, ax = plt.subplots()
    ax.plot(f,mytrace_1min)
    ax.plot(REF_IMG,0,'^k') # ###    
    plt.title(my_samples[S_IDX])
    ax.set_xticks(np.arange(0,NR_FRAMES,50))
    ax.set_xticks(np.arange(0,NR_FRAMES,10), minor=True)
    ax.grid(axis = 'x', which='minor')
    ax.grid(axis = 'x', which='major')
    
    
    plt.savefig(my_out_dir+'correlation_function_calibration_'+my_samples[S_IDX]+'.pdf')
    # plt.show()
    
# Some code to identify the index of a specific dataset
# This code can be ignored
if False: 
    [i for i in range(len(my_samples)) if my_samples[i] == '2023-03-15-MW-PC-epi-titrate.lif_B2-p1-nt']
    [i for i in range(len(my_samples)) if my_samples[i] == '2023-03-15-MW-PC-epi-titrate.lif_B2-p2-nt']

    [i for i in range(len(my_samples)) if my_samples[i] == '2023-03-15-MW-PC-epi-titrate.lif_B4-p1-nt']
    [i for i in range(len(my_samples)) if my_samples[i] == '2023-03-15-MW-PC-epi-titrate.lif_B2-p2-nt-r2']


# Now put this information in the excel file, re-load the excel file with the
# code at the beginning, and execute this section again to make sure all plots
# look good.



###############################################################################
# Another plot (redundant, can be ignored)

f=np.array(range(0,NR_FRAMES))
t=f*sample_dt[my_samples[S_IDX]]
mytrace_1min = np.array([1-val for val in mytrace])

my_dpi=600

major_ticks = np.arange(0, np.max(t), 1)
minor_ticks = np.arange(0, np.max(t), 1)

fig = plt.figure(figsize=(10/2.54, 10/2.54), dpi=my_dpi)      

ax=fig.add_subplot(1, 1, 1)
plt.plot(t,mytrace_1min)
ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='major')
plt.title(my_samples[S_IDX])
plt.xlabel('Time (s)')
plt.ylabel('Correlation with image '+str(REF_IMG))
plt.xlim((0, 5))

plt.show()

###############################################################################
# Difference with reference image
# (Not used any more, can be ignored..)

# See line 748 other script
frs_of_interest = [location_closest_value(t, t_show)[0] for t_show in [1, 1.2, 1.4, 1.6, 1.8, 2]]


current_ref_img_path = my_image_base+str(REF_IMG).zfill(4)+'.tif'
ref_img = readimg_roi(current_ref_img_path, roi)

image_series = [readimg_roi(my_image_base+str(fr).zfill(4)+'.tif', roi) for fr in frs_of_interest]

# Use 1st image as reference
image_series_delta = [img-image_series[0] for img in image_series]

# Ref image correlation-ref-image
#image_series_delta = [img-ref_img for img in image_series]

overall_min = np.min(image_series_delta)
overall_max = np.max(image_series_delta)

# Single image
#imgplot = plt.imshow(image_series[4]-ref_img)
#plt.show()

###############################################################################
# Create a nice figure
# (Not used any more, can be ignored..)

fig = plt.figure(figsize=(10/2.54,10/2.54), dpi=600) 

# Plot the trace
ax=fig.add_subplot(3, 1, 1)
plt.plot(t,mytrace_1min)
plt.plot(t[frs_of_interest],mytrace_1min[frs_of_interest], 'ko')
ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='major')
plt.title(my_samples[S_IDX])
plt.xlabel('Time (s)')
plt.ylabel('1-Corr with image '+str(REF_IMG))
plt.xlim((0, 5))

for ii in range(len(frs_of_interest)):

    fr_of_interest = frs_of_interest[ii]
    # fr_of_interest=frs_of_interest[0]
        
    print('fr '+str(fr_of_interest))
    
    ax=fig.add_subplot(3, 6, 1*6+ii+1)
    
    current_img=image_series_delta[ii]
                 
    # Create little example movies
    ax = plt.imshow(current_img, vmin=overall_min, vmax=overall_max,
                   cmap=plt.get_cmap('hot'), interpolation='nearest')
    #plt.colorbar(ax)
    plt.axis('off')    
    
    ax=fig.add_subplot(3, 6, 2*6+ii+1)
    
    current_img=image_series[ii]
                 
    # Create little example movies
    ax = plt.imshow(current_img,
                   cmap=plt.get_cmap('hot'), interpolation='nearest')
    #plt.colorbar(ax)
    plt.axis('off')    
    
    #plt.title('Image @ t_adj='+str(np.round(t_adj[fr_of_interest],2))+' seconds')

plt.tight_layout()
plt.show()

fig.savefig(my_out_dir+'custom_example_contr-corr_'+my_samples[S_IDX]+'_img.pdf')







###############################################################################
###############################################################################
# Contractility-plot based on correlation again
# Same as above, but now automated over samples
# NOTE THAT THIS TAKES LONG!

# TO DO:
# Implement storing the cropped images

NR_FRAMES = 1500 # frames 1 .. NR_FRAMES will be considered for the analysis
    # I now did 500 but there are already 4 datasets where it's better to 
    # take 1000 frames; probably best to repeat this analysis with the max
    # amount of frames and just store that data. (In this case, max 'd be 2000.)

list_traces_corrcontr = {}
for S_IDX in range(len(my_samples)):
    
    # In case there are some exception-cases, this allows easy manual updating
    # S_IDX = 18; NR_FRAMES = 1000 
    # S_IDX = 23; NR_FRAMES = 1000    
    # S_IDX = 30; NR_FRAMES = 1000
    # S_IDX = 24; NR_FRAMES = 1000    
    
    # For convenience, give user some information
    print("Working on sample " + my_samples[S_IDX]+', '+str(S_IDX+1)+'/'+str(len(my_samples)))
    current_date_and_time = datetime.now()
    print(str(current_date_and_time))
    
    # Get parameters
    REF_IMG = sample_refimg[my_samples[S_IDX]]
    roi = sample_roi[my_samples[S_IDX]]
    
    # Example of correlation calculation
    # thecorr, p = stats.pearsonr([1,2,3],[1,2,2])
    
    # Image path base
    my_image_base = my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'
    
    # Now loop over images and correlate image with original image
    # note that I aimed for a frame rate of ±40fps, so if it beats
    # every 10 secs, i need to analyze 400 images ..
    refimage_path = my_image_base+str(REF_IMG).zfill(4)+'.tif'
    img_ref = mpimg.imread(refimage_path)
    mytrace=[]
    for img_idx in range(0, NR_FRAMES):
        imgageXXXX_path = my_image_base+str(img_idx).zfill(4)+'.tif'
        img_XXXX = mpimg.imread(imgageXXXX_path)
        R,p=stats.pearsonr(img_ref[roi[0]:roi[1],roi[2]:roi[3]].flatten(),
                         img_XXXX[roi[0]:roi[1],roi[2]:roi[3]].flatten())
        mytrace.append(R)
        if (img_idx%200==0):
            print(str(round(img_idx/NR_FRAMES*100,1))+'% done..')
            
    list_traces_corrcontr[my_samples[S_IDX]] = mytrace
            
# Little bit of debugging
# (You can ignore this code.)
if False:
    my_samples[S_IDX]
    plt.imshow(img_ref[roi[0]:roi[1],roi[2]:roi[3]])
    plt.imshow(img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
    
# Explicitly save this parameter, to skip the lengthy part of the analysis
# later.
if not os.path.exists(my_work_dir+"saved_data/"):
    os.mkdir(my_work_dir+"saved_data/")
current_date_and_time = datetime.now()
current_date = current_date_and_time.strftime("%Y-%m-%d")
pickle.dump( list_traces_corrcontr, open( my_work_dir+"saved_data/"+current_date+"_list_traces_corrcontr.p", "wb" ) )
# To load, use
# list_traces_corrcontr = pickle.load( open( my_work_dir+"saved_data/"+"2023-04-03"+"_list_traces_corrcontr.p", "rb" ) )
    
###############################################################################
# Now post-process these signals (creates plots to double check what's done)

# Establish peaks and 1-signal
PEAKMINTIME = .5 # estimate of minimum distance between peaks
SMOOTHINGTIME = .2 # estimate of minimum distance between peaks
PEAKMINHEIGHT = .7 # expressed as quantile
first_peaks = {}
second_peaks = {}
first_peak_height = {}
list_traces_1min = {}
list_minvals={}
list_maxvals={}

for S_IDX in range(len(my_samples)):
    
    current_trace      = list_traces_corrcontr[my_samples[S_IDX]]    
    current_trace_1min = np.array([1-val for val in current_trace])

    f = np.arange(0,len(current_trace))
    
    # estimate time scale for peaks in terms of frames
    current_distance = int(round(PEAKMINTIME/sample_dt[my_samples[S_IDX]]))
    current_smoothing_window = int(round(SMOOTHINGTIME/sample_dt[my_samples[S_IDX]]))
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
    req_height=np.quantile(current_trace_1min_sav, PEAKMINHEIGHT)
    peaks_in_mytrace_pos, _ = signal.find_peaks(current_trace_1min_sav, distance=current_distance, height=req_height)            
    
    # Take the 2nd peak as first peak, as sometimes the data starts within a peak
    # leading to artifacts
    current_firstpeak = peaks_in_mytrace_pos[1]
    current_second_peak = peaks_in_mytrace_pos[2]
    
    # collect results
    first_peaks[my_samples[S_IDX]] = current_firstpeak
    second_peaks[my_samples[S_IDX]] = current_second_peak    
    list_traces_1min[my_samples[S_IDX]] = current_trace_1min
    list_minvals[my_samples[S_IDX]]=np.quantile(current_trace_1min_sav, .02)
    list_maxvals[my_samples[S_IDX]]=np.quantile(current_trace_1min_sav, .98)
    first_peak_height[my_samples[S_IDX]]=current_trace_1min[current_firstpeak]
    
    # plot
    plt.plot(f, current_trace_1min)
    plt.plot(f,     current_trace_1min_sav, '--r')
    plt.plot(current_firstpeak, current_trace_1min[current_firstpeak],'ko')
    plt.plot(current_second_peak, current_trace_1min[current_second_peak],'ko')    
    plt.title('ID: '+my_samples[S_IDX]+' ('+str(S_IDX)+')')
    #plt.ylim((0.06,0.09))
    
    plt.savefig(my_out_dir+'peakfinder_corr_'+my_samples[S_IDX]+'_img.pdf')
    plt.show()



###############################################################################
# Create aligned plots, in two panels


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

SEARCHTERMS = ['-nt$','-nt-t','p1-EPI-t2$','p2-EPI-t3$','p1-EPI-t4$']
mycolors    = ['b'  ,'b'  ,'r'        ,'r'      ,'r']

peak_durations_50 = {}

fig = plt.figure(figsize=(10/2.54,10/2.54), dpi=600) 

peak_durations={}
peak_durations_byterm={T:np.empty(0) for T in SEARCHTERMS} 
interpeak_times={}
interpeak_times_byterm={T:np.empty(0) for T in SEARCHTERMS}
first_peak_height_byterm = {T:np.empty(0) for T in SEARCHTERMS}
for idx_t in range(len(SEARCHTERMS)):
    
    current_SEARCHTERM = SEARCHTERMS[idx_t]
    
    ax=fig.add_subplot(len(SEARCHTERMS), 1, idx_t+1)
    
    # selected_samples = [sample for sample in my_samples if current_SEARCHTERM in sample]
    selected_samples = [sample for sample in my_samples if re.search(current_SEARCHTERM, sample)]   
    for sample_name in selected_samples:
        
        current_trace             = list_traces_1min[sample_name]        
        NR_FRAMES                 = len(current_trace)       
        current_firstpeak         = first_peaks[sample_name]
        current_second_peak       = second_peaks[sample_name]    
        current_first_peak_height = first_peak_height[sample_name]        
        current_firstpeak_time    = current_firstpeak*sample_dt[sample_name]
        current_t                 = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
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
        peak_durations[sample_name] = peak_duration_50*sample_dt[sample_name]
        peak_durations_byterm[current_SEARCHTERM] = np.append(peak_durations_byterm[current_SEARCHTERM],peak_duration_50*sample_dt[sample_name])
        interpeak_times[sample_name] = interpeak_frames*sample_dt[sample_name]
        interpeak_times_byterm[current_SEARCHTERM] = np.append(interpeak_times_byterm[current_SEARCHTERM],interpeak_frames*sample_dt[sample_name])
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

plt.savefig(my_out_dir+'final_overview_traces.pdf')
plt.show()

plt.close('all') 





# For now, I manually exported some of this data to Prism
peak_durations_byterm
interpeak_times_byterm
first_peak_height_byterm




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





