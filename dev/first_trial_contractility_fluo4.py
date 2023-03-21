#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:53:10 2022

@author: m.wehrens
"""

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

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)

my_work_dir  = '/Volumes/Wehrens_Mic/IMG_ANALYSIS/2022-12-16/2022.12.16_Fluo4_test/'

sample_info  = pd.read_excel(my_work_dir+'sample_info.xlsx')
my_samples = sample_info['sample_name'].to_numpy()

my_out_dir   = my_work_dir+'out/'

if not (os.path.isdir(my_out_dir)):
    os.mkdir(my_out_dir)

###############################################################################

# Import custom functions
import sys
sys.path.append("/Users/m.wehrens/Documents/git_repos/cardio_img_analysis/functions/")
from custom_functions_contractility import *

###############################################################################
# Custom functions

"""
# Autocorrelation function
def acf(x, length=1500):
    return np.array([1]+[np.corrcoef(x[:-i], x[i:])[0,1]  \
        for i in range(1, length)])


# Find a (closest) value in array function
def location_closest_value(x, val):
    dx = np.abs(np.array(x)-np.array(val))
    return( [i for i in range(len(dx)) if dx[i] == np.min(dx)] )
"""

###############################################################################
# Show an initial image for testing

#my_image_dir = '/Volumes/workdrive_m.wehrens_hubrecht/microscopy_images/pictures/'
#my_image = 'pilot-4nov_b1_pos1_movie_t0000.tif'
#my_image_base = 'pilot-4nov_b1_pos1_movie_t'
#my_image_path = my_image_dir+my_image

img_idx = 0
img = mpimg.imread(my_work_dir+my_samples[0]+'/'+my_samples[0]+'/'+my_samples[0]+'_t'+str(img_idx).zfill(4)+'.tif')

# normalize image
# note that the signal will vary from one image to the next
# so we don't want to normalize on single-image basis in the eventual analysis
img_norm = (img-np.min(img))/(np.max(img)-np.min(img))

imgplot = plt.imshow(img_norm)
plt.show()


###############################################################################
# Go over all images to determine maxima

my_maxtraces_list={}
for DATA_IDX in range(0,len(my_samples)):
    # DATA_IDX=1
    
    print("Starting sample "+str(DATA_IDX)+'/'+str(len(my_samples))+" ==============")
    
    my_maxvalues=[]
    for img_idx in range(0, 3000):
    
        img = mpimg.imread(my_work_dir+my_samples[DATA_IDX]+'/'+my_samples[DATA_IDX]+'/'+my_samples[DATA_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')
        my_maxvalues.append(np.max(img))        
    
        if (img_idx%150==0):
            print(str(np.round(img_idx/3000*100,2))+'% done..')
            
    my_maxtraces_list[my_samples[DATA_IDX]] = my_maxvalues

# Show the trace of maxes
plt.plot(my_maxvalues)
plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
plt.xlabel('frame')
plt.ylabel('fluo4 signal (a.u.)')
plt.ylim((0, np.max(my_maxvalues)*1.1))
plt.show()

###############################################################################
# Overview of max traces
fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_trace = my_maxtraces_list[my_samples[DATA_IDX]]
    
    plt.plot(current_trace)
    #plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
    plt.title(my_samples[DATA_IDX])
    #plt.xlabel('frame')
    #plt.ylabel('fluo4 signal (a.u.)')
    plt.ylim((0, np.max(current_trace)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('np.max(img) over time')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()

#fig.savefig(my_output_dir+'my_plot.tif')

###############################################################################
# So this immediately shows a challenge, which is that the fluorescence 
# signal seems to be decreasing (due to bleaching, probably)

# Let's try to fit an exponential decay curve trough this for all plots
my_fitted_maxes_list={}

for DATA_IDX in range(0,len(my_samples)):
    
    current_trace = np.array(my_maxtraces_list[my_samples[DATA_IDX]], dtype=np.float32)
    logtrace = np.log(current_trace)
    x=np.arange(0,3000)
    myfit = np.polyfit(x, logtrace, 3)
    fity=np.exp(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])

    my_fitted_maxes_list[my_samples[DATA_IDX]] = fity


###############################################################################
# Plot again maxima with fits

fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_trace = my_maxtraces_list[my_samples[DATA_IDX]]
    current_fity  = my_fitted_maxes_list[my_samples[DATA_IDX]]
    
    plt.plot(current_trace)
    plt.plot(current_fity)    
    #plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
    plt.title(my_samples[DATA_IDX])
    #plt.xlabel('frame')
    #plt.ylabel('fluo4 signal (a.u.)')
    plt.ylim((0, np.max(current_trace)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('np.max(img) over time')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()

# Fitting for one curve
"""
DATA_IDX=0
plt.plot(np.log(my_maxtraces_list[my_samples[DATA_IDX]]))
plt.show()

current_trace = np.array(my_maxtraces_list[my_samples[DATA_IDX]], dtype=np.float32)
logtrace = np.log(current_trace)
x=np.arange(0,3000)
myfit = np.polyfit(x, logtrace, 3)
fity=np.exp(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])
plt.plot(current_trace)
plt.plot(fity)
plt.show()

plt.plot(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])
plt.plot(np.log(current_trace))
plt.show()
"""

###############################################################################
# Show a subsection of one image


# Take a random image
img_idx = 0
img = mpimg.imread(my_work_dir+my_samples[0]+'/'+my_samples[0]+'/'+my_samples[0]+'_t'+str(img_idx).zfill(4)+'.tif')
# normalize image
img_norm = (img-np.min(img))/(np.max(img)-np.min(img))

# Note that the images come in waves, so pro'lly convenient to take 
# a section in the middle to make sure we're not smoothing temporal effects
#
# Total image is 256x256, take a ±center part at 51*2 : 51*3 --> 102:153
roi_c1=102
roi_c2=153
roi_r1=102
roi_r2=153

sub_img = img_norm[roi_c1:roi_c2,roi_r1:roi_r2]

imgplot = plt.imshow(sub_img)
plt.show()



###############################################################################
# Go over all images and determine the mean from the middle section of the image

roi_c1=102
roi_c2=153
roi_r1=102
roi_r2=153

my_meantraces_list={}
for DATA_IDX in range(0,len(my_samples)):
    # DATA_IDX=1
    
    print("Starting sample "+str(DATA_IDX)+'/'+str(len(my_samples))+" ==============")
    
    my_meanvalues=[]
    for img_idx in range(0, 3000):
    
        img = mpimg.imread(my_work_dir+my_samples[DATA_IDX]+'/'+my_samples[DATA_IDX]+'/'+my_samples[DATA_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')
        my_meanvalues.append(np.mean(img[roi_c1:roi_c2,roi_r1:roi_r2]))        
    
        if (img_idx%150==0):
            print(str(np.round(img_idx/3000*100,2))+'% done..')
            
    my_meantraces_list[my_samples[DATA_IDX]] = my_meanvalues

# Show the trace of a mean value
plt.plot(my_meantraces_list[my_samples[DATA_IDX]])
plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
plt.xlabel('frame')
plt.ylabel('fluo4 signal (a.u.)')
plt.ylim((0, np.max(my_meantraces_list[my_samples[DATA_IDX]])*1.1))
plt.show()

# Now a normalized version
current_trace = my_meantraces_list[my_samples[DATA_IDX]]
current_trace_norm = current_trace/my_fitted_maxes_list[my_samples[DATA_IDX]]
plt.plot(current_trace_norm)
plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
plt.xlabel('frame')
plt.ylabel('fluo4 signal (a.u.)')
plt.ylim((0, np.max(current_trace_norm)*1.1))
plt.show()


###############################################################################
# Now plot the mean plots

fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_trace = my_maxtraces_list[my_samples[DATA_IDX]]
    current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
    current_fity  = my_fitted_maxes_list[my_samples[DATA_IDX]]
        
    plt.plot(current_meantrace/current_fity)  
    #plt.plot(current_fity)
    #plt.title("np.max(img) plotted over time ("+my_samples[DATA_IDX]+")")
    plt.title(my_samples[DATA_IDX])
    #plt.xlabel('frame')
    #plt.ylabel('fluo4 signal (a.u.)')
    plt.ylim((np.min(current_meantrace/current_fity)*.9, np.max(current_meantrace/current_fity)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('np.max(img) over time')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()

###############################################################################
# Work out better normalization

DATA_IDX=0

current_trace = my_maxtraces_list[my_samples[DATA_IDX]]
current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
current_fity  = my_fitted_maxes_list[my_samples[DATA_IDX]]

# need to find local 
plt.plot(current_meantrace) 
plt.show()

# let's find the locations of the local minima peaks



current_meantrace_32 = np.array(current_meantrace, dtype=np.float32)
log_current_trace = np.log(current_meantrace_32)
x=np.arange(0,3000)
myfit = np.polyfit(x, log_current_trace, 3)
fity=np.exp(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])

peaks_in_mytrace_pos, _ = signal.find_peaks(current_meantrace_32/fity, distance=40)

plt.plot(current_meantrace_32/fity) 
#plt.plot(fity) 
plt.plot(x[peaks_in_mytrace_pos], current_meantrace_32[peaks_in_mytrace_pos]/fity[peaks_in_mytrace_pos],'ro') 
plt.xlim((0,500))
plt.show()

plt.plot(current_meantrace/fity) 
plt.show()

negative_meantrace = current_meantrace * np.array(-1.0, dtype=np.float32)

peaks_in_mytrace, _ = signal.find_peaks(negative_meantrace[0:500], distance=40)


plt.plot(negative_meantrace[0:500]) 
plt.plot(x[peaks_in_mytrace],negative_meantrace[peaks_in_mytrace],'ro') 
plt.show()

# Use the correlation function to estimate inter-peak time

        
mytrace_correlation = acf(current_meantrace_32)
peaks_in_cor, _ = signal.find_peaks(mytrace_correlation)

plt.plot(mytrace_correlation)
plt.plot(np.arange(0,500)[peaks_in_cor], mytrace_correlation[peaks_in_cor],'ro')
plt.show()

# now use the distance between two peaks as input for the baseline fit by negative peaks
peak_est_distance = peaks_in_cor[2]-peaks_in_cor[1]
peaks_in_mytrace, _ = signal.find_peaks(negative_meantrace, distance=peak_est_distance*.6)
plt.plot(current_meantrace_32) 
plt.plot(x[peaks_in_mytrace],current_meantrace_32[peaks_in_mytrace]) 
plt.show()

# now create a fit again to this
myfit = np.polyfit(x[peaks_in_mytrace], np.log(current_meantrace_32[peaks_in_mytrace]), 3)
fity=np.exp(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])
plt.plot(current_meantrace_32) 
plt.plot(fity) 
plt.show()


###############################################################################
# Now do this for all traces
     
my_baselinetraces={}
peak_est_distances_list={}
for DATA_IDX in range(0,len(my_samples)):
    # DATA_IDX=1
    
    # collect the data
    current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
    current_meantrace_32 = np.array(current_meantrace, dtype=np.float32)    

    # get the correlation, and get the interpeak-time estimate 
    mytrace_correlation = acf(current_meantrace_32)
    peaks_in_cor, _ = signal.find_peaks(mytrace_correlation)

    # now use the distance between two peaks as input for the baseline fit by negative peaks
    # using 60% of interpeak time as minimum distance for local minima
    negative_meantrace=current_meantrace_32*np.array(-1,dtype=np.float32)
    peak_est_distance = peaks_in_cor[2]-peaks_in_cor[1]
    peaks_in_mytrace, _ = signal.find_peaks(negative_meantrace, distance=peak_est_distance*.6)

    # now create a baseline fit using this info
    myfit = np.polyfit(x[peaks_in_mytrace], np.log(current_meantrace_32[peaks_in_mytrace]), 3)
    baseline_fit=np.exp(myfit[3]+x**1*myfit[2]+x**2*myfit[1]+x**3*myfit[0])

    # save 'm
    my_baselinetraces[my_samples[DATA_IDX]]=baseline_fit
    peak_est_distances_list[my_samples[DATA_IDX]]=peak_est_distance
      
    
###############################################################################
# Now show all traces with the baseline fits

fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
    current_baselinefit  = my_baselinetraces[my_samples[DATA_IDX]]
        
    plt.plot(current_meantrace)  
    plt.plot(current_baselinefit)    

    plt.title(my_samples[DATA_IDX])

    plt.ylim((np.min(current_meantrace)*.9, np.max(current_meantrace)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('trace&fitted baseline over time')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()

###############################################################################
# Now show again the traces, but divided by baseline


fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
    current_baselinefit  = my_baselinetraces[my_samples[DATA_IDX]]
        
    plt.plot(current_meantrace/current_baselinefit)  

    plt.title(my_samples[DATA_IDX])

    plt.ylim((np.min(current_meantrace/current_baselinefit)*.9, np.max(current_meantrace/current_baselinefit)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('trace normalized w/ baseline')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()


###############################################################################
# Determine the time-dependent normalization factors for each of the movies
# For movie normalization, it is slightly complicated to normalize propoerly
# because of the broader trent present in the data
# 
# The overall idea would be to fit a line through the peaks in the data
# This is however complicated because the peaks are hard to recognize
# by algorithms (due to broader trend and noisy signal).
#
# My solution now is to fit a curve to the complete signal, and then
# determine maxima as a percentage of the signal using the fit,
# and then using that percentage to extrapolate (shift up) the fitted line
# to now fit the maxima.

normalizationbymax_pct_list={}
normalizationbymax_pctmax_list={}
normalizationbymax_trace_list={}
for DATA_IDX in range(0,len(my_samples)):

    current_maxtrace        = my_maxtraces_list[my_samples[DATA_IDX]]
    current_maxtrace_expfit = my_fitted_maxes_list[my_samples[DATA_IDX]]
    current_meantrace       = my_meantraces_list[my_samples[DATA_IDX]]
    current_baselinefit     = my_baselinetraces[my_samples[DATA_IDX]]    
    
    my_estimated_pct_max    = np.max(current_maxtrace/current_maxtrace_expfit)
    normalizationbymax_pctmax_list[my_samples[DATA_IDX]]   = my_estimated_pct_max
    my_estimated_pct_tile   = np.percentile(current_maxtrace/current_maxtrace_expfit, 99)*1.01    
    normalizationbymax_pct_list[my_samples[DATA_IDX]]      = my_estimated_pct_tile
    normalizationbymax_trace_list[my_samples[DATA_IDX]]    = current_maxtrace_expfit*my_estimated_pct_tile

# Now plot all these
fig = plt.figure(figsize=(40/2.54,40/2.54), dpi=600) # figsize=(10, 7)
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    fig.add_subplot(5, 5, DATA_IDX+1)
    
    current_maxtrace        = my_maxtraces_list[my_samples[DATA_IDX]]
    current_maxtrace_expfit = my_fitted_maxes_list[my_samples[DATA_IDX]]
    current_meantrace       = my_meantraces_list[my_samples[DATA_IDX]]
    current_baselinefit     = my_baselinetraces[my_samples[DATA_IDX]]  
       
    # current_normalizationbymax_pct = normalizationbymax_pct_list[my_samples[DATA_IDX]]
    current_normalizationbymax_trace = normalizationbymax_trace_list[my_samples[DATA_IDX]]
    
    plt.plot(current_maxtrace)  
    plt.plot(current_maxtrace_expfit)   
    plt.plot(current_normalizationbymax_trace) 

    plt.title(my_samples[DATA_IDX])

    plt.ylim((np.min(current_maxtrace)*.9, np.max(current_maxtrace)*1.1))
    
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("frame")
plt.ylabel("fluo4 signal (a.u.)")    

fig.suptitle('trace&fitted max values over time')
fig.tight_layout()  
#fig.suptitle('np.max(img) over time')
plt.show()

###############################################################################
# Now make a custom comparison
datasets_nt = ['w1-p2-1hz-nt', 'w1-p3-1hz-nt', 'w5-p1-1hz-nt', 'w5-p2-1hz-nt', 'w5-p3-1hz-nt']
datasets_iso = ['w1-p4-1hz-iso', 'w1-p5-1hz-iso', 'w1-p6-1hz-iso', 'w5-p5-1hz-iso', 'w5-p7-1hz-iso', 'w5-p8-1hz-iso']

CUSTOM_X = 5

# scale w/ time in seconds
t = np.arange(0,3000)/3000*30.04
major_ticks = np.arange(0, 30, 5)
minor_ticks = np.arange(0, 30, 1)

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 

ax=fig.add_subplot(2, 2, 1)
plt.plot(t, my_meantraces_list[datasets_nt[0]]/my_baselinetraces[datasets_nt[0]])
plt.title('NT')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(2, 2, 2)
plt.plot(t, my_meantraces_list[datasets_nt[1]]/my_baselinetraces[datasets_nt[1]])
plt.xlim((0,10))
plt.title('NT')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(2, 2, 3)
plt.plot(t, my_meantraces_list[datasets_iso[0]]/my_baselinetraces[datasets_iso[0]])
plt.xlim((0,10))
plt.title('ISO')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(2, 2, 4)
plt.plot(t, my_meantraces_list[datasets_iso[1]]/my_baselinetraces[datasets_iso[1]])
plt.xlim((0,10))
plt.title('ISO')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.xlim((0,CUSTOM_X))

plt.show()

###############################################################################
# There doesn't really seem to be that much of signal,
# so let's try to align the curves for more precise investigation

# concept
trace1_nt = my_meantraces_list[datasets_nt[0]]/my_baselinetraces[datasets_nt[0]]
peaks_in_mytrace, _ = signal.find_peaks(trace1_nt, distance=peak_est_distances_list[datasets_nt[0]]*.6)
second_peak = peaks_in_mytrace[1]
peaks_in_mytrace_inv, _ = signal.find_peaks(-trace1_nt, distance=peak_est_distances_list[my_samples[DATA_IDX]]*.6)
second_peak_inv = peaks_in_mytrace_inv[1]
plt.plot(t,trace1_nt)
plt.plot(t[second_peak],    trace1_nt[second_peak],'ro')
plt.plot(t[second_peak_inv],trace1_nt[second_peak_inv],'bo')
plt.xlim((0,5))
plt.show()

plt.plot(t,-trace1_nt)
plt.plot(t[second_peak_inv],-trace1_nt[second_peak_inv],'bo')
plt.xlim((0,5))
plt.show()

# Calculate time corrections
time_corrections_list_idx = {}
time_corrections_list = {}
time_corrections_inv_list_idx = {}
time_corrections_inv_list = {}
for DATA_IDX in range(0,len(my_samples)):
    #DATA_IDX=0
    
    current_meantrace = my_meantraces_list[my_samples[DATA_IDX]]
    current_baselinefit  = my_baselinetraces[my_samples[DATA_IDX]]

    current_trace_normalized = current_meantrace/current_baselinefit

    # identify positive peaks
    peaks_in_mytrace, _ = signal.find_peaks(current_trace_normalized, distance=peak_est_distances_list[my_samples[DATA_IDX]]*.6)
    second_peak = peaks_in_mytrace[1]

    time_corrections_list_idx[my_samples[DATA_IDX]]=second_peak
    time_corrections_list[my_samples[DATA_IDX]]=t[second_peak]

    # identify negative peaks (ie start of peak)
    # peaks_in_mytrace_inv, _ = signal.find_peaks(-current_trace_normalized, distance=peak_est_distances_list[my_samples[DATA_IDX]]*.6)
    
    # for the inverse, perform slight filter (smoothign)
    current_trace_normalized_sav = signal.savgol_filter(current_trace_normalized, window_length, 3)
    peaks_in_mytrace_inv, _ = signal.find_peaks(-current_trace_normalized_sav, distance=peak_est_distances_list[my_samples[DATA_IDX]]*.6)
    
    second_peak_inv = peaks_in_mytrace_inv[1]

    time_corrections_inv_list_idx[my_samples[DATA_IDX]]=second_peak_inv
    time_corrections_inv_list[my_samples[DATA_IDX]]=t[second_peak_inv]

# example of filter
window_length = int(peak_est_distances_list[my_samples[DATA_IDX]]*.2)
if (window_length%2==0):
    window_length=window_length+1
yhat=signal.savgol_filter(current_trace_normalized, window_length, 3)    
plt.plot(yhat)


for DATA_ID in datasets_nt[0:4]:
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    
plt.xlim((0,10))
plt.title('NT')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.show()





for DATA_ID in datasets_iso[0:4]:
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    
plt.xlim((0,10))
plt.title('ISO')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.show()



###############################################################################
# A custom figure with some points of interest


# First show the trace
# scale w/ time in seconds
CUSTOM_X=5
DATA_ID = 'w1-p2-1hz-nt' 
DATA_ID = 'w1-p4-1hz-iso' 
# my_samples[4] # 'w1-p2-1hz-nt'
#DATA_ID = 'w1-p3-1hz-nt' # 
t = np.arange(0,3000)/3000*30.04
major_ticks = np.arange(0, 30, 5)
minor_ticks = np.arange(0, 30, 1)

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 

# dt_adj = time_corrections_list[DATA_ID]
dt_adj = time_corrections_inv_list[DATA_ID] # start of peak
t_adj=t-dt_adj

# Determine frames of interest
# find closest value
# fr_of_interest = location_closest_value(t, 1+dt_adj)
frs_of_interest = [location_closest_value(t, t_show+dt_adj)[0] for t_show in [1, 1.2, 1.4, 1.6, 1.8]]

#fig = plt.figure(figsize=(800/my_dpi, 1600/my_dpi), dpi=my_dpi)  
fig = plt.figure(figsize=(1500/my_dpi, 1500/my_dpi), dpi=my_dpi)      

ax=fig.add_subplot(3, 1, 1)
plt.plot(t_adj, my_meantraces_list[DATA_ID]/my_baselinetraces[DATA_ID])
y_=my_meantraces_list[DATA_ID]/my_baselinetraces[DATA_ID]
plt.plot(t_adj[frs_of_interest], y_[frs_of_interest],'ro')
plt.title(DATA_ID)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='minor')
plt.xlim((0,CUSTOM_X))

# preliminary loop to determine additional normalization factor
overall_min=np.inf
overall_max=0.0
for ii in range(len(frs_of_interest)):
    
    fr_of_interest = frs_of_interest[ii] 
    # fr_of_interest=frs_of_interest[0]

    norm_factor = normalizationbymax_trace_list[DATA_ID][fr_of_interest]    
    img = mpimg.imread(my_work_dir+DATA_ID+'/'+DATA_ID+'/'+DATA_ID+'_t'+str(fr_of_interest).zfill(4)+'.tif')[roi_c1:roi_c2,roi_r1:roi_r2,0]
    img_norm = img / norm_factor
    overall_max = np.max([np.max(img_norm), overall_max])
    overall_min = np.min([np.min(img_norm), overall_min])    
    
for ii in range(len(frs_of_interest)):

    fr_of_interest = frs_of_interest[ii]
    # fr_of_interest=frs_of_interest[0]
        
    norm_factor = normalizationbymax_trace_list[DATA_ID][fr_of_interest]
    
    print('fr '+str(fr_of_interest)+' (norm='+str(norm_factor)+')')
    
    ax=fig.add_subplot(3, 5, 5+ii+1)
    
    img_complete = mpimg.imread(my_work_dir+DATA_ID+'/'+DATA_ID+'/'+DATA_ID+'_t'+str(fr_of_interest).zfill(4)+'.tif')[:,:,0]
    img_complete_norm = img_complete/norm_factor
    
    img = img_complete[roi_c1:roi_c2,roi_r1:roi_r2]
    img_norm = img / norm_factor
                 
    # Create little example movies
    ax = plt.imshow(img_norm, vmin=overall_min, vmax=overall_max,
                   cmap=plt.get_cmap('hot'), interpolation='nearest')
    #plt.colorbar(ax)
    plt.axis('off')
    
    ax = fig.add_subplot(3, 5, 10+ii+1)
    ax = plt.imshow(img_complete_norm, vmin=overall_min, vmax=overall_max,
                   cmap=plt.get_cmap('hot'), interpolation='nearest')
    plt.axis('off')
    
    #plt.title('Image @ t_adj='+str(np.round(t_adj[fr_of_interest],2))+' seconds')

plt.show()


# Direct comparison
CUSTOM_X=5
fig = plt.figure(figsize=(1500/my_dpi, 300/my_dpi), dpi=my_dpi)  
ax = fig.add_subplot(1, 1, 1)
major_ticks = np.arange(0, 30, 1)
minor_ticks = np.arange(0, 30, 1)

for DATA_ID in ['w1-p2-1hz-nt' , 'w1-p4-1hz-iso' ]:
    
    dt_adj = time_corrections_inv_list[DATA_ID] # start of peak
    t_adj=t-dt_adj
    
    f_show_end = location_closest_value(t_adj, CUSTOM_X)[0]
    y  = (my_meantraces_list[DATA_ID]/my_baselinetraces[DATA_ID])[0:f_show_end]
    y_ = (y-np.min(y))/(np.max(y)-np.min(y))
    
    plt.plot(t_adj[0:f_show_end], y_, label=DATA_ID)

#ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))
plt.legend(loc='upper right')

#ax.set_xticks(major_ticks)
#ax.set_xticks(minor_ticks, minor=True)
plt.grid(axis = 'x')






###############################################################################
# Custom figure to show in grant proposal
# (Copy of above but edited a bit)



# First show the trace
# scale w/ time in seconds
CUSTOM_X=5
DATA_ID = 'w1-p2-1hz-nt' 
# my_samples[4] # 'w1-p2-1hz-nt'
#DATA_ID = 'w1-p3-1hz-nt' # 
t = np.arange(0,3000)/3000*30.04
major_ticks = np.arange(0, 30, 1)
minor_ticks = np.arange(0, 30, 1)

fig = plt.figure(figsize=(10/2.54,6/2.54), dpi=600) 
#fig = plt.figure(figsize=(800/my_dpi, 1600/my_dpi), dpi=my_dpi)  
#fig = plt.figure(figsize=(1500/my_dpi, 800/my_dpi), dpi=my_dpi)      

# dt_adj = time_corrections_list[DATA_ID]
dt_adj = time_corrections_inv_list[DATA_ID] # start of peak
t_adj=t-dt_adj

# Determine frames of interest
# find closest value
# fr_of_interest = location_closest_value(t, 1+dt_adj)
frs_of_interest = [location_closest_value(t, t_show+dt_adj)[0] for t_show in [1, 1.2, 1.4, 1.6, 1.8]]

# dt_adj = time_corrections_list[DATA_ID]
dt_adj = time_corrections_inv_list[DATA_ID] # start of peak
t_adj=t-dt_adj

# Determine frames of interest
# find closest value
# fr_of_interest = location_closest_value(t, 1+dt_adj)
frs_of_interest = [location_closest_value(t, t_show+dt_adj)[0] for t_show in [1, 1.2, 1.4, 1.6, 1.8]]

# Plot the trace
ax=fig.add_subplot(2, 1, 1)
plt.plot(t_adj, my_meantraces_list[DATA_ID]/my_baselinetraces[DATA_ID])
y_=my_meantraces_list[DATA_ID]/my_baselinetraces[DATA_ID]
plt.plot(t_adj[frs_of_interest], y_[frs_of_interest],'ko')
plt.title('Calcium currents, pacing 1 Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x')#, which='minor')
plt.xlabel('Time (s)')
plt.ylabel('Fluo4 signal (a.u.)')
plt.xlim((0,CUSTOM_X))
plt.yticks([])

# preliminary loop to determine additional normalization factor
overall_min=np.inf
overall_max=0.0
for ii in range(len(frs_of_interest)):
    
    fr_of_interest = frs_of_interest[ii] 
    # fr_of_interest=frs_of_interest[0]

    norm_factor = normalizationbymax_trace_list[DATA_ID][fr_of_interest]    
    img = mpimg.imread(my_work_dir+DATA_ID+'/'+DATA_ID+'/'+DATA_ID+'_t'+str(fr_of_interest).zfill(4)+'.tif')[roi_c1:roi_c2,roi_r1:roi_r2,0]
    img_norm = img / norm_factor
    overall_max = np.max([np.max(img_norm), overall_max])
    overall_min = np.min([np.min(img_norm), overall_min])    
    
for ii in range(len(frs_of_interest)):

    fr_of_interest = frs_of_interest[ii]
    # fr_of_interest=frs_of_interest[0]
        
    norm_factor = normalizationbymax_trace_list[DATA_ID][fr_of_interest]
    
    print('fr '+str(fr_of_interest)+' (norm='+str(norm_factor)+')')
    
    ax=fig.add_subplot(2, 5, 5+ii+1)
    
    img_complete = mpimg.imread(my_work_dir+DATA_ID+'/'+DATA_ID+'/'+DATA_ID+'_t'+str(fr_of_interest).zfill(4)+'.tif')[:,:,0]
    img_complete_norm = img_complete/norm_factor
    
    img = img_complete[roi_c1:roi_c2,roi_r1:roi_r2]
    img_norm = img / norm_factor
                 
    # Create little example movies
    ax = plt.imshow(img_norm, vmin=overall_min, vmax=overall_max,
                   cmap=plt.get_cmap('hot'), interpolation='nearest')
    #plt.colorbar(ax)
    plt.axis('off')    
    
    #plt.title('Image @ t_adj='+str(np.round(t_adj[fr_of_interest],2))+' seconds')

plt.tight_layout()
plt.show()

fig.savefig(my_out_dir+'custom_example_fluo4_'+DATA_ID+'_img.pdf')



###############################################################################
# Comparison plots

# Comparison of unpaced and paced
###
CUSTOM_X=6
major_ticks = np.arange(0, 30, 5)
minor_ticks = np.arange(0, 30, 1)

fig = plt.figure(figsize=(22/2.54,20/2.54), dpi=600) 

ax=fig.add_subplot(3, 1, 1)

# NT, 1 Hz
for DATA_ID in ['w1-p1-nopacing','w5-p1-nopacing']: # 'w1-p2-1hz-nt','w1-p3-1hz-nt', 
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized, label=DATA_ID)
    

plt.legend(loc="upper right")
plt.title('NT, No pacing')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(3, 1, 2)

# NT, 1 Hz
for DATA_ID in ['w1-p2-1hz-nt','w1-p3-1hz-nt','w5-p1-1hz-nt','w5-p2-1hz-nt','w5-p3-1hz-nt']: # 'w1-p5-1hz-iso','w1-p6-1hz-iso',
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized, label=DATA_ID)
    

plt.legend(loc="upper right")
plt.title('NT 1Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(3, 1, 3)

# NT, 2 Hz
for DATA_ID in ['w1-p2-2hz-nt','w1-p3-2hz-nt','w5-p1-2hz-nt','w5-p2-2hz-nt','w5-p3-2hz-nt']: # 'w1-p5-1hz-iso','w1-p6-1hz-iso',
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized, label=DATA_ID)
    

plt.legend(loc="upper right")
plt.title('NT 2Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

plt.show()







# 1Hz comparison
###
CUSTOM_X=5
major_ticks = np.arange(0, 30, 5)
minor_ticks = np.arange(0, 30, 1)

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 

ax=fig.add_subplot(2, 1, 1)

# NT, 1 Hz
for DATA_ID in ['w1-p2-1hz-nt','w1-p3-1hz-nt']: # 'w5-p1-1hz-nt', 'w5-p2-1hz-nt'
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    

plt.title('NT, 1Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(2, 1, 2)

# ISO, 1 Hz
for DATA_ID in ['w1-p5-1hz-iso','w1-p6-1hz-iso']: # 'w5-p7-1hz-iso','w5-p8-1hz-iso'
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    

plt.title('ISO 1Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

plt.show()









# 2Hz comparison
###
CUSTOM_X=5
major_ticks = np.arange(0, 30, 5)
minor_ticks = np.arange(0, 30, .5)

fig = plt.figure(figsize=(20/2.54,20/2.54), dpi=600) 

ax=fig.add_subplot(2, 1, 1)

# NT, 2 Hz
for DATA_ID in ['w5-p1-2hz-nt', 'w5-p2-2hz-nt']:
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    

plt.title('NT, 2Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

ax=fig.add_subplot(2, 1, 2)

# ISO, 2 Hz
for DATA_ID in ['w5-p6-2hz-iso','w5-p7-2hz-iso']:
    current_meantrace = my_meantraces_list[DATA_ID]
    current_baselinefit  = my_baselinetraces[DATA_ID]

    current_trace_normalized = current_meantrace/current_baselinefit
    
    t_adjusted=t-time_corrections_list[DATA_ID]
    
    plt.plot(t_adjusted,current_trace_normalized)
    

plt.title('ISO 2Hz')
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(axis = 'x', which='both')
plt.xlim((0,CUSTOM_X))

plt.show()



###############################################################################
# Create little movies

roi_c1=102
roi_c2=153
roi_r1=102
roi_r2=153

my_dpi=300

t = np.arange(0,3000)/3000*30.04

for DATA_ID in ['w1-p2-1hz-nt','w5-p5-1hz-iso']:

    if not (os.path.isdir(my_out_dir+DATA_ID)):
        os.mkdir(my_out_dir+DATA_ID)

    for fr_idx in np.arange(0,400,4):    

        img = mpimg.imread(my_work_dir+DATA_ID+'/'+DATA_ID+'/'+DATA_ID+'_t'+str(fr_idx).zfill(4)+'.tif')
        img_norm = img
        fig = plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)        

        # Create little example movies
        plt.imshow(img_norm[roi_c1:roi_c2,roi_r1:roi_r2])
        plt.title('Image @ '+str(np.round(t[fr_idx],2))+' seconds')
        
        fig.savefig(my_out_dir+DATA_ID+'/'+DATA_ID+'_img_'+str(fr_idx)+'.tif')
        plt.close()
        
        
        



