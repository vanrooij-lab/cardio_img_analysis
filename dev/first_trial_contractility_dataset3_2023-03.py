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

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)

###############################################################################


def readimg_roi(path, roi):
    img = mpimg.imread(path)[:,:,0]
    roi_img = img[roi[0]:roi[1],roi[2]:roi[3]]
    
    return roi_img

###############################################################################

my_work_dir = '/Volumes/Wehrens_Mic/IMG_ANALYSIS/2022-12-16/2022.12.16_DES_siRNA/'

my_out_dir   = my_work_dir+'out/'

if not (os.path.isdir(my_out_dir)):
    os.mkdir(my_out_dir)

###############################################################################

# Sample information

sample_info  = pd.read_excel(my_work_dir+'sample_info_20221216_DES.xlsx')

# Sample list
my_samples = sample_info['sample_name'].to_numpy()

# Dict with frame time
sample_info['dt'] = sample_info['duration_movie']/sample_info['total_frames']
sample_dt = {sample_info['sample_name'][ii]:sample_info['dt'][ii] for ii in range(len(sample_info))}
sample_roi_ = {sample_info['sample_name'][ii]:sample_info['roi'][ii] for ii in range(len(sample_info))} # read ROI as string
sample_roi  = {key:[int(x) for x in sample_roi_[key].replace('\ufeff','').split(', ')] for key in sample_roi_.keys()} # convert strings to int
sample_refimg = {sample_info['sample_name'][ii]:sample_info['ref_frame'][ii] for ii in range(len(sample_info))}
 
###############################################################################

S_IDX = 17 # sample index

###############################################################################
# Load image and show it

#my_image_dir = '/Volumes/workdrive_m.wehrens_hubrecht/microscopy_images/pictures/'
#my_image = 'pilot-4nov_b1_pos1_movie_t0000.tif'
#my_image_base = 'pilot-4nov_b1_pos1_movie_t'
#my_image_path = my_image_dir+my_image

img_idx=0
img_ = mpimg.imread(my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')

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

imgplot = plt.imshow(img_norm)
plt.show()

###############################################################################
# Determine a region for this image set

roi_=cv2.selectROI('ROI_select', img_norm)
roi = [roi_[1],  roi_[3]+roi_[1], roi_[0], roi_[2]+roi_[0]]
    # roi_ = x1, y1, dx, dy; but x and y reversal somewhere
    # roi = [y1,y2,x1,x2]

cv2.destroyWindow('ROI_select') 
cv2.waitKey(1) # required due to buggy cv2/gtk behavior https://stackoverflow.com/questions/6116564/destroywindow-does-not-close-window-on-mac-using-python-and-opencv

imgplot = plt.imshow(img_norm[roi[0]:roi[1],roi[2]:roi[3]])
plt.show()

roi

###############################################################################

# Output all ROIs for the images
for S_IDX in range(len(my_samples)):
    
    img_ = mpimg.imread(my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'+str(img_idx).zfill(4)+'.tif')
    img_norm = (img-np.min(img))/(np.max(img)-np.min(img))
    
    current_roi = sample_roi[my_samples[S_IDX]]
    
    imgplot = plt.imshow(img_norm[current_roi[0]:current_roi[1],current_roi[2]:current_roi[3]])
    
    plt.savefig(my_out_dir+'ROI_'+my_samples[S_IDX]+'.pdf')
    plt.show()
    
    
###############################################################################
###############################################################################
# Calculate the correlation using the first frame as reference
# FOR ONE SAMPLE ONLY

S_IDX=17
REF_IMG = 20
NR_FRAMES = 500

# Example of correlation calculation
# thecorr, p = stats.pearsonr([1,2,3],[1,2,2])

my_image_base = my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'

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

###############################################################################
# Simple plot w/ frame nrs & grid

f=np.array(range(0,NR_FRAMES))
mytrace_1min = np.array([1-val for val in mytrace])
fig, ax = plt.subplots()
ax.plot(f,mytrace_1min)
ax.set_xticks(np.arange(0,NR_FRAMES,50))
ax.set_xticks(np.arange(0,NR_FRAMES,10), minor=True)
ax.grid(axis = 'x', which='minor')
ax.grid(axis = 'x', which='major')
plt.show()

###############################################################################
# Somewhat sophisticated plot (grid lines @ 1s)

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
# Same as above, but now AUTOMATED OVER SAMPLES

list_traces_corrcontr = {}
for S_IDX in range(len(my_samples)):
    
    print("Working on sample " + my_samples[S_IDX])
    
    REF_IMG = sample_refimg[my_samples[S_IDX]]
    NR_FRAMES = 500
    
    # Example of correlation calculation
    # thecorr, p = stats.pearsonr([1,2,3],[1,2,2])
    
    my_image_base = my_work_dir+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'/'+my_samples[S_IDX]+'_t'
    
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
        if (img_idx%50==0):
            print(str(img_idx/NR_FRAMES*100)+'% done..')
            
    list_traces_corrcontr[my_samples[S_IDX]] = mytrace
            

# Establish peaks and 1-signal
PEAKMINTIME = .5 # estimate of minimum distance between peaks
SMOOTHINGTIME = .2 # estimate of minimum distance between peaks
PEAKMINHEIGHT = .7 # expressed as quantile
first_peaks = {}
list_traces_1min = {}
list_minvals={}
list_maxvals={}
f=np.arange(0,NR_FRAMES)
for S_IDX in range(len(my_samples)):
    
    current_trace      = list_traces_corrcontr[my_samples[S_IDX]]    
    current_trace_1min = np.array([1-val for val in current_trace])
    
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
    current_firstpeak = peaks_in_mytrace_pos[0]
    
    # collect results
    first_peaks[my_samples[S_IDX]] = current_firstpeak
    list_traces_1min[my_samples[S_IDX]] = current_trace_1min
    list_minvals[my_samples[S_IDX]]=np.quantile(current_trace_1min_sav, .02)
    list_maxvals[my_samples[S_IDX]]=np.quantile(current_trace_1min_sav, .98)
    
    # plot
    plt.plot(f, current_trace_1min)
    plt.plot(f,     current_trace_1min_sav, '--r')
    plt.plot(current_firstpeak, current_trace_1min[current_firstpeak],'ko')
    plt.title('ID: '+my_samples[S_IDX]+' ('+str(S_IDX)+')')
    #plt.ylim((0.06,0.09))
    plt.show()

###############################################################################
# Create aligned plots, in two panels

NR_FRAMES = 500

fig = plt.figure(figsize=(10/2.54,10/2.54), dpi=600) 

ax=fig.add_subplot(2, 1, 1)
samples_scrambled1hz = [sample for sample in my_samples if 'scrambled-1hz' in sample]
for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'b-')
    
plt.ylim((-.2,1.2))  
plt.xlim((-.5,1.5))  
plt.title('Scrambled siRNA')
# Add grids
ax.set_xticks(np.arange(-.5,1.5+.1,.5))
ax.set_xticks(np.arange(-.5,1.5+.1,.1), minor=True)
ax.grid(axis = 'x', which='minor')
ax.grid(axis = 'x', which='major')

ax=fig.add_subplot(2, 1, 2)
samples_siDes1hz = [sample for sample in my_samples if 'siDES-1hz' in sample]
for sample_name in samples_siDes1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'r-')

plt.ylim((-.2,1.2))
plt.xlim((-.5,1.5))  
plt.title('DES siRNA')
# Add grids
ax.set_xticks(np.arange(-.5,1.5+.1,.5))
ax.set_xticks(np.arange(-.5,1.5+.1,.1), minor=True)
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
# Create aligned plots, on top of each other

NR_FRAMES = 500

fig = plt.figure(figsize=(7/2.54,7/2.54), dpi=600) 

ax=fig.add_subplot(1, 1, 1)
samples_scrambled1hz = [sample for sample in my_samples if 'scrambled-1hz' in sample]
for sample_name in samples_scrambled1hz:
    
    current_firstpeak      = first_peaks[sample_name]
    current_firstpeak_time = current_firstpeak*sample_dt[sample_name]
    current_t              = np.arange(0,NR_FRAMES)*sample_dt[sample_name]
    current_t_adj          = current_t-current_firstpeak_time
    current_trace          = list_traces_1min[sample_name]
    current_trace_norm     = (current_trace-list_minvals[sample_name])/(list_maxvals[sample_name]-list_minvals[sample_name])
    
    plt.plot(current_t_adj, current_trace_norm,'b-', linewidth=.5)
       
samples_siDes1hz = [sample for sample in my_samples if 'siDES-1hz' in sample]
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

samples_scrambled1hz = [sample for sample in my_samples if 'scrambled-1hz' in sample]

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





