#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:53:10 2022

@author: m.wehrens
"""

# Let's try to in a very simple way process the beating heart cell images


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#import cv2
import numpy as np

import scipy.stats as stats

import scipy.signal as signal

import os

my_output_dir = '/Volumes/workdrive_m.wehrens_hubrecht/microscopy_images/python_analysis/out/'

my_image_dir = '/Volumes/workdrive_m.wehrens_hubrecht/microscopy_images/pictures/'
my_image = 'pilot-4nov_b1_pos1_movie_t0000.tif'
my_image_base = 'pilot-4nov_b1_pos1_movie_t'
my_image_path = my_image_dir+my_image

img = mpimg.imread(my_image_dir+my_image)

imgplot = plt.imshow(img)
plt.show()

112, 912
640, 1504

imgplot = plt.imshow(img[912:1504, 111:640])
plt.show()

###############################################################################

# Some image-specific settings

frame_interval = 38.885/3955 # in seconds


# ROI for b1.pos1
roi_c1=912
roi_c2=1504
roi_r1=111
roi_r2=640

imgplot = plt.imshow(img[roi_c1:roi_c2,roi_r1:roi_r2])
plt.show()

###############################################################################
# Calculate the correlation with the first frame

# Example of correlation calculation
# thecorr, p = stats.pearsonr([1,2,3],[1,2,2])

# Now loop over images and correlate image with original image
# note that I aimed for a frame rate of ±40fps, so if it beats
# every 10 secs, i need to analysze 400 images ..
image0_path = my_image_dir+my_image_base+str(0).zfill(4)+'.tif'
img_0000 = mpimg.imread(image0_path)
mytrace=[]
for img_idx in range(0, 1000):
    imgageXXXX_path = my_image_dir+my_image_base+str(img_idx).zfill(4)+'.tif'
    img_XXXX = mpimg.imread(imgageXXXX_path)
    R,p=stats.pearsonr(img_0000[roi_c1:roi_c2,roi_r1:roi_r2].flatten(),
                     img_XXXX[roi_c1:roi_c2,roi_r1:roi_r2].flatten())
    mytrace.append(R)
    if (img_idx%10==0):
        print(str(img_idx/1000*100)+'% done..')

###############################################################################

# Now also find the peaks

mytrace_cut = np.array(mytrace)
mytrace_cut[mytrace_cut<(max(mytrace)*.9)]=0 
peaks_in_mytrace, _ = signal.find_peaks(mytrace_cut)
peak_times = frame_interval*peaks_in_mytrace

###############################################################################

###############################################################################
# Now show the trace, showing peaks
# Also calculate inter-peak times

t=np.array(range(0,1000))
mytrace_arr=np.array(mytrace)
plt.plot(t,mytrace)
plt.plot(t[peaks_in_mytrace],mytrace_arr[peaks_in_mytrace],'ro')
plt.xlabel('frame')
plt.ylabel('Correlation with image 0')
plt.title("Trace v0")
plt.show()

dt = peak_times[1:]-peak_times[:len(peak_times)-1]

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





