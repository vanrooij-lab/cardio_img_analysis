#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:19:51 2023

@author: m.wehrens
"""

import numpy as np

import pandas as pd

import matplotlib.image as mpimg
import cv2 # installed using terminal and pip; "pip install opencv-python"
import matplotlib.pyplot as plt

import os
from datetime import datetime 

import scipy.stats as stats

import scipy.signal as signal

import re

###############################################################################


def readimg_roi(path, roi):
    img = mpimg.imread(path)[:,:,0]
    roi_img = img[roi[0]:roi[1],roi[2]:roi[3]]
    
    return roi_img



###############################################################################
# Custom functions

# Autocorrelation function
def acf(x, length=1500):
    return np.array([1]+[np.corrcoef(x[:-i], x[i:])[0,1]  \
        for i in range(1, length)])


# Find a (closest) value in array function
def location_closest_value(x, val):
    dx = np.abs(np.array(x)-np.array(val))
    return( [i for i in range(len(dx)) if dx[i] == np.min(dx)] )

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

###############################################################################
# This function interactively allows you to select the ROI for each of the samples

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

###############################################################################
# Output the ROIs for each of the samples as images

def output_ROIs(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, ROI_dir, uptowhichsample=None):
    # Define the frame that is used to take an image
    img_idx = 0
    
    if uptowhichsample is None:
        uptowhichsample=len(sample_info_dicts['name']) # all samples
    
    # Output all ROIs for the images
    for S_IDX in range(uptowhichsample):

        # Load the image
        img = mpimg.imread(my_work_dir+sample_info_dicts['name'][S_IDX]+'/'+sample_info_dicts['name'][S_IDX]+\
                            '_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'.tif')
        img_norm = (img-np.min(img))/(np.max(img)-np.min(img))

        # What are the ROI coordinates?
        current_roi = sample_info_dicts['roi'][sample_info_dicts['name'][S_IDX]]

        # Plot it
        F = plt.figure()
        imgplot = plt.imshow(img_norm[current_roi[0]:current_roi[1],current_roi[2]:current_roi[3]], cmap = 'gray')    
        plt.title(sample_info_dicts['name'][S_IDX])
        plt.savefig(ROI_dir+'ROI_'+sample_info_dicts['name'][S_IDX]+'.pdf')
        plt.close(F)

###############################################################################
# Extract and store the cropped regions from the original data, 
# to be used for later analysis

def generate_cropped_data(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, ZIPCROPPED, samples_to_do=None, mycropsubdir='data_cropped'):
    """By giving a custom range via samples_to_do you can set s custom range of samples to do."""

    if samples_to_do is None:
        samples_to_do = range(len(sample_info_dicts['name']))

    # Create the directory to store the cropped data
    if not os.path.exists(my_work_dir+mycropsubdir):
        os.mkdir(my_work_dir+mycropsubdir)

    # Loop over the different samples
    for S_IDX in samples_to_do:

        # For convenience, give user some information
        print("Working on sample " + sample_info_dicts['name'][S_IDX]+', '+\
              str(S_IDX+1)+'/'+str(len(sample_info_dicts['name'])))
        current_date_and_time = datetime.now()
        print(str(current_date_and_time))

        # Get parameters
        roi = sample_info_dicts['roi'][sample_info_dicts['name'][S_IDX]]

        # Image path base
        my_image_dir = my_work_dir+sample_info_dicts['name'][S_IDX]+'/'

        if not os.path.exists(my_work_dir+mycropsubdir+'/CROP_'+sample_info_dicts['name'][S_IDX]+'/'):
            os.mkdir(my_work_dir+mycropsubdir+'/CROP_'+sample_info_dicts['name'][S_IDX]+'/')

        # Loop over the frames within this sample
        for img_idx in range(0, NR_FRAMES):

            # Retrieve image XXX
            my_img_filename = sample_info_dicts['name'][S_IDX]+'_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX  
            imgageXXXX_path = my_image_dir+my_img_filename+'.tif'
            img_XXXX = mpimg.imread(imgageXXXX_path)

            # Save the cropped image
            if ZIPCROPPED:
                np.savez_compressed(my_work_dir+mycropsubdir+'/CROP_'+sample_info_dicts['name'][S_IDX]+'/'+   my_img_filename+'_cropped.npz'    ,\
                                    img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
            else:
                np.save(my_work_dir+mycropsubdir+'/CROP_'+sample_info_dicts['name'][S_IDX]+'/'+   my_img_filename+'_cropped.npy'    ,\
                                    img_XXXX[roi[0]:roi[1],roi[2]:roi[3]])
                # print(my_work_dir+mycropsubdir+'/CROP_'+my_img_filename)

            # User progress
            if (img_idx%200==0):
                print(str(round(img_idx/NR_FRAMES*100,1))+'% done..')

###############################################################################
# Preliminary calculation of the correlation using a given frame as reference, 
# to calibrate the frames of references.
# These reference frames will need to be calibrated, so this procedure might
# need to be iterated; therefor this will output each of the plots, and you
# should update the reference frames in the excel file, such that they
# lie outside a beating motion. when they lie within a beating motion,
# this will also result in the whole plot looking "weird". then, reload the excel 
# file, and repeat the procedure, until all reference frames are appropriate.          

def calculate_preliminary_correlation(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, PREANA_dir, samples_to_do=None):

    if samples_to_do is None:
        samples_to_do = range(len(sample_info_dicts['name']))

    for S_IDX in samples_to_do:
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


###############################################################################
        

def run_correlation_analysis(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, samples_to_do=None):
   
    if samples_to_do is None:
        samples_to_do = range(len(sample_info_dicts['name']))

    list_traces_corrcontr = {}
    for S_IDX in samples_to_do:
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
        
    return list_traces_corrcontr
    

###############################################################################
# Now post-process these signals 
# This both creates plots of the signals, but also 
# extracts some features of interest, like the distance between peaks,
# peak width, peak height (not so useful), etc..

def find_features_and_plot(sample_info_dicts, list_traces_corrcontr, my_out_dir, samples_to_do=None, PEAKMINTIME   = .5, SMOOTHINGTIME = .2, PEAKMINHEIGHT = .8):
    
    # This allows user to set samples_to_do to run a subset of the samples
    if samples_to_do is None:
        samples_to_do = range(len(sample_info_dicts['name']))
    
    # These parameters will be returned, and contain the important features
    first_peaks = {}
    second_peaks = {}
    first_peak_height = {}
    list_traces_1min = {}
    list_minvals={}
    list_maxvals={}

    # Loop over samples
    for S_IDX in samples_to_do:

        print(str(S_IDX))

        # Fetch the trace
        current_trace      = list_traces_corrcontr[sample_info_dicts['name'][S_IDX]]    
        current_trace_1min = np.array([1-val for val in current_trace])
        # Frames
        f = np.arange(0,len(current_trace))

        # estimate time scale for peaks in terms of frames
        current_distance = int(round(PEAKMINTIME/sample_info_dicts['dt'][sample_info_dicts['name'][S_IDX]]))
        current_smoothing_window = int(round(SMOOTHINGTIME/sample_info_dicts['dt'][sample_info_dicts['name'][S_IDX]]))
        if (current_smoothing_window % 2 == 0):
            current_smoothing_window += 1

        # smooth data
        current_trace_1min_sav = signal.savgol_filter(current_trace_1min, current_smoothing_window, 3)

        # First identify the first peak in each one
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
        plt.plot(f, current_trace_1min_sav, '--r')
        plt.plot(current_firstpeak, current_trace_1min[current_firstpeak],'ko')
        plt.plot(current_second_peak, current_trace_1min[current_second_peak],'ko')    
        plt.title('ID: '+sample_info_dicts['name'][S_IDX]+' ('+str(S_IDX)+')')
        plt.savefig(my_out_dir+'analysis/peakfinder_corr_'+sample_info_dicts['name'][S_IDX]+'_img.pdf')
        # plt.show()

        plt.close()

    return first_peaks, second_peaks, first_peak_height, \
            list_traces_1min, list_minvals, list_maxvals



###############################################################################
# Final analysis, to create aligned plots, and to extract important peak features
# grouped per search term

def create_plots_extract_final_features(sample_info, sample_info_dicts, \
                         list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
                         SEARCHTERMS, mycolors, XMAX, my_out_dir):

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
    #plt.show()

    plt.close('all') 

    # Return the values
    return peak_durations, peak_durations_byterm, interpeak_times, interpeak_times_byterm, \
                first_peak_height_byterm, selected_samples_list_byterm

###############################################################################

def test_lib_load():
    print('This is a test')
    return

print('hoi123202403')