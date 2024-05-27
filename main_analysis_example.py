#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:53:10 2022

THIS SCRIPT IS USED TO ANALYZE THE CONTRACTILITY OF CARDIOMYOCYTES
CURRENTLY, THIS IS THE LASTEST VERSION OF THIS SCRIPT...
    -- 2024/03/12

Note on 2024/03/12:
    I reorganized the code such that all important code is now
    organized in functions. The file is based on the file
    time_ale_contractility_dataset2_2023-10-11_edited202403.py
    but that file is now deleted and renamed into this file. 
    (will be done next commit)   

    This allows for easier recycling of the code for other datasets.

    The functions are stored in the files custom_functions_contractility and 
    custom_functions_movies.

    I tested the code, but it's not yet fully tested, so there might be some
    bugs when it's executed!

    I now moved this file into the main directory, as an example of 
    how to perform your analysis.

    Some discarded part of the script can be found in the file 
    time_ale_contractility_dataset2_2023-10-11_edited202403_discarded-parts.py
    and might still be useful later.
    

@author: m.wehrens
"""

################################################################################
# First load libraries required for this script


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

font = {'family' : 'Arial', # earlier set to 'normal'
    'weight' : 'bold',
    'size'   : 8}

matplotlib.rc('font', **font)

import pickle

# Custom functions
import sys
sys.path.append("/Users/m.wehrens/Documents/git_repos/cardio_img_analysis/functions/")
#from custom_functions_contractility import *
#from custom_functions_movies import *

import custom_functions_contractility as cuslibc
import custom_functions_movies as cuslibm

import numpy as np
from scipy import signal


    # importlib.reload(cuslibc)
    # importlib.reload(cuslibm)


###############################################################################

# Load previously analyzed data:

# Note that using the standard save option from Spyder ("spydata" format) fails
# to load the file because of pickle issue.
# https://stackoverflow.com/questions/55890813/how-to-fix-object-arrays-cannot-be-loaded-when-allow-pickle-false-for-imdb-loa

# I'm going to do manual pickle at the end.
# Use the following line to load previous analysis:
    
# list_traces_corrcontr = pickle.load( open( my_work_dir+"saved_data/"+"2023-04-03"+"_list_traces_corrcontr.p", "rb" ) )

###############################################################################
# Define parameters specific for this analysis

IMGNAMESUFFIX='_ch00'

my_work_dir = '/Volumes/Wehrens_Mic/RAW_DATA/2023-XX-XX/TIF_ORGANIZED/'

# For plate 2
# my_out_dir   = '/Volumes/Wehrens_Mic/RAW_DATA/2023-10-11_Analysis/Analysis_Plate2/'
# sample_annotation_filepath = my_out_dir+'2023_10_11_Tim_Ale__positions_CM.xlsx'

# For plate 1 (note: choose to execute either plate 1 or plate 2 code)
my_out_dir   = '/Users/m.wehrens/Data/__other_analyses/contractility/Thomas/extra_output_Martijn/'
sample_annotation_filepath = '/Users/m.wehrens/Data/__other_analyses/contractility/Thomas/files_Thomas/2024_04_26_SuJi_Thomas_baseline_RX_CM_diff4.xlsx'

if not (os.path.isdir(my_out_dir)): 
    os.mkdir(my_out_dir)

###############################################################################
# This loads the sample meta data from the excel file
# You might need to execute this sectino multiple times to "refresh" the
# parameters when you update them in the excel.

sample_info, sample_info_dicts =\
    cuslibc.read_sample_information(sample_annotation_filepath)
   
    
###############################################################################
# Create a series of movies, using custom scripted function loaded above
# Note that I only look at first 500 frames, skipping 10 frames, because
# it's too much data otherwise, and this suits purposes.

movies_out_dir=my_out_dir+'movies_python_auto/'

if not (os.path.isdir(movies_out_dir)): 
    os.mkdir(movies_out_dir)

# Full run
cuslibm.create_movies(sample_info, my_work_dir, movies_out_dir)

# Partial run
# cuslibm.create_movies(sample_info, my_work_dir, movies_out_dir, subsel=2)

###############################################################################

S_IDX = 1 # sample index

###############################################################################
# Determine a region for this image set
# Put this in the excel file, and then reload information from the excel 
# file again

# Only determine ROI for user-selected samples, since some samples
# might be from the same position, so we want to later customize
# ROIs such that they are consistent between those positions.
# SELECTED_SAMPLES = ['2023_03_29.lif_A1-p1-nt', '2023_03_29.lif_A1-p2-nt', '2023_03_29.lif_A2-p1-nt', '2023_03_29.lif_A2-p2-nt', '2023_03_29.lif_B1-p1-nt', '2023_03_29.lif_B1-p2-nt', '2023_03_29.lif_B2-p1-nt', '2023_03_29.lif_B2-p2-nt']

# Here, all samples are selected that have a a flag "create_movie" set to "yes
SELECTED_SAMPLES = sample_info['sample_name'][sample_info['create_movie']=='yes'].values

# Now collect the ROIs
collected_ROIs = cuslibc.define_ROIs(my_work_dir, SELECTED_SAMPLES, IMGNAMESUFFIX)
    # testing purposes 
    # collected_ROIs = cuslibc.define_ROIs(my_work_dir, SELECTED_SAMPLES[0:4], IMGNAMESUFFIX)
# Print them
collected_ROIs

# And export them to an excel file
df_ROI = \
    pd.DataFrame({
                    'Sample name':collected_ROIs.keys(),
                    'ROI':[str(v).replace('[','').replace(']','') for v in collected_ROIs.values()]  })
df_ROI.to_excel(my_out_dir+'automatic_ROIs.xlsx')

# Now add the above values manually into the annotation excel file, and reload the excel file 
# information using the line below.
sample_info, sample_info_dicts = cuslibc.read_sample_information(sample_annotation_filepath)

###############################################################################
# Output all ROI regions as images

# Define a directory to store the ROIs as images
ROI_dir = my_out_dir+'ROIs/'
if not (os.path.isdir(ROI_dir)): 
    os.mkdir(ROI_dir)

# Call the function
cuslibc.output_ROIs(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, ROI_dir)
    
###############################################################################

# See the script:    
# time_ale_contractility_dataset2_2023-10-11_EXTENSIONS.py
# for additional custom plots.
        



###############################################################################
###############################################################################
# Create a folder with cropped data
# So that the correlation analysis can be done on the cropped data
# This is done to save time, as the correlation analysis is very time-consuming.
# NOTE THAT THIS TAKES LONG!

from datetime import datetime # for some reason throws error otherwise ..

# Some parameters
ZIPCROPPED = False
NR_FRAMES = 1500 # frames 1 .. NR_FRAMES will be considered for the analysis
    # I now did 500 but there are already 4 datasets where it's better to 
    # take 1000 frames; probably best to repeat this analysis with the max
    # amount of frames and just store that data. (In this case, max 'd be 2000.)

# Call the function
cuslibc.generate_cropped_data(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, ZIPCROPPED)

    # Or perform a test run 
    # cuslibc.generate_cropped_data(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES=10, ZIPCROPPED=False, samples_to_do=range(2), mycropsubdir='data_cropped2')
            

###############################################################################
###############################################################################
# Preliminary calculation of the correlation using a given frame as reference, 
# to calibrate the frames of references.
# These reference frames will need to be calibrated, so this procedure might
# need to be iterated; therefor this will output each of the plots, and you
# should update the reference frames in the excel file, such that they
# lie outside a beating motion. when they lie within a beating motion,
# this will also result in the whole plot looking "weird". then, reload the excel 
# file, and repeat the procedure, until all reference frames are appropriate.   

PREANA_dir = my_out_dir+'pre-analysis/'
if not (os.path.isdir(PREANA_dir)): 
    os.mkdir(PREANA_dir)

# S_IDX=0
# REF_IMG = 85
NR_FRAMES = 250

# This doesn't do anything, but might be convenient to check out the names
sample_info_dicts['name']

# Execute the function to calculate the preliminary correlation
cuslibc.calculate_preliminary_correlation(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, PREANA_dir) # , samples_to_do=range(3))
    # Testing purposes
    # cuslibc.calculate_preliminary_correlation(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES, PREANA_dir, samples_to_do=range(3))

# Now update reference frames in the excel file, re-load the excel file with the
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

    
# Execute the function to generate the correlations that represent the cardiomyocyte beating traces.
list_traces_corrcontr = cuslibc.run_correlation_analysis(sample_info_dicts, my_work_dir, IMGNAMESUFFIX, NR_FRAMES) # , samples_to_do=range(2))

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
# list_traces_corrcontr = pickle.load( open( my_out_dir+"saved_data_py/"+"2023-10-16"+"_list_traces_corrcontr.p", "rb" ) )

###############################################################################
# Now post-process these signals 
# This both creates plots of the signals, but also 
# extracts some features of interest, like the distance between peaks,
# peak width, peak height (not so useful), etc..

if not os.path.exists(my_out_dir+"analysis/"):
    os.mkdir(my_out_dir+"analysis/")

import matplotlib.pyplot as plt

# Important parameters required for the analysis
PEAKMINTIME   = .5 # estimate of minimum distance between peaks, in seconds
SMOOTHINGTIME = .2 # width of smoothing window, in seconds 
PEAKMINHEIGHT = .8 # minimum height of peak, expressed as quantile

# Call the function which plots traces and analyzes important features    
first_peaks, second_peaks, first_peak_height, list_traces_1min, list_minvals, list_maxvals = \
        cuslibc.find_features_and_plot(sample_info_dicts, list_traces_corrcontr, my_out_dir, 
                            PEAKMINTIME=PEAKMINTIME, SMOOTHINGTIME=SMOOTHINGTIME, PEAKMINHEIGHT=PEAKMINHEIGHT) 
                            # , samples_to_do=range(3)) # for testing purposes

# Some debugging
if False:
    
    plt.hist(current_trace_1min_sav, color='lightgreen', ec='black', bins=15)
    np.quantile(current_trace_1min_sav, 1)
    np.quantile(current_trace_1min_sav, .8)      
    np.quantile(current_trace_1min_sav, .7)    
    np.quantile(current_trace_1min_sav, PEAKMINHEIGHT)



###############################################################################
###############################################################################

# The analysis is now done, you can proceed with extracting the values, 
# and exporting them to an excel file, and then do some further analysis
#
# However, below a graph is created, and that code also re-organizes
# the data in a more convenient way to export it to excel.

###############################################################################
###############################################################################



###############################################################################
# Let's re-organize the data and export it to excel
# 
# Multiple aligned plots, in two panels, but now also calculate some 
# parameters of interest

XMAX = 3.5

SEARCHTERMS = ['before_no-treatment$',     'after_no-treatment$', 
               'before_spiny-FB$',       'after_spiny-FB$', 'before_mus-FB$', 'after_mus-FB$', 
               'before_spiny-FB-medium$', 'after_spiny-FB-medium$', 'before_mus-FB-medium$',      'after_mus-FB-medium$']
mycolors    = ['b','r',
               'b','r','b','r',
               'b','r','b','r']


# Now run the function which determines (extra) features of interest and groups them by search terms.
#peak_durations, peak_durations_byterm, interpeak_times, interpeak_times_byterm, \
#                first_peak_height_byterm, selected_samples_list_byterm = \
#    cuslibc.create_plots_extract_final_features(sample_info, sample_info_dicts, \
#                            list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
#                            SEARCHTERMS, mycolors, XMAX, my_out_dir)

# Now run the function which determines (extra) features of interest and groups them by search terms.
# UPDATED WITH CONTRACTION AND RELAXATION DURATIONS
peak_durations, peak_durations_byterm, interpeak_times, interpeak_times_byterm, \
                first_peak_height_byterm, selected_samples_list_byterm, \
                durations_contraction, durations_relaxation, durations_contraction_fraction, durations_relaxation_fraction, \
                durations_contraction_byterm, durations_relaxation_byterm, durations_contraction_fraction_byterm, durations_relaxation_fraction_byterm = \
    cuslibc.create_plots_extract_final_features(sample_info, sample_info_dicts, \
                            list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
                            SEARCHTERMS, mycolors, XMAX, my_out_dir)



# Now also call an additional function that determines the contractile and relaxation periods
durations_contraction, durations_relaxation, durations_contraction_fraction, durations_relaxation_fraction, \
                durations_contraction_byterm, durations_relaxation_byterm, durations_contraction_fraction_byterm, durations_relaxation_fraction_byterm = \
    cuslibc.determine_contractile_times(sample_info, sample_info_dicts, \
                         list_traces_1min, first_peaks, second_peaks, first_peak_height, list_minvals, list_maxvals, \
                         interpeak_times, \
                         SEARCHTERMS, mycolors, XMAX, my_out_dir,
                         PEAK_BASE_FRACTION=0.05)


# For now, I manually exported some of this data to Prism
peak_durations_byterm
interpeak_times_byterm
first_peak_height_byterm
selected_samples_list_byterm
# and contractily period times
durations_contraction_byterm
durations_relaxation_byterm
durations_contraction_fraction_byterm
durations_relaxation_fraction_byterm

# Export to excel
df_to_export = \
    pd.concat(
        [pd.DataFrame({
                    'peak_duration':peak_durations_byterm[SEARCHTERMS[idx]],
                    'interpeak':interpeak_times_byterm[SEARCHTERMS[idx]],
                    'peak_height':first_peak_height_byterm[SEARCHTERMS[idx]],
                    'duration_contraction':durations_contraction_byterm[SEARCHTERMS[idx]],
                    'durations_relaxation':durations_relaxation_byterm[SEARCHTERMS[idx]],
                    'durations_contraction_fraction':durations_contraction_fraction_byterm[SEARCHTERMS[idx]],
                    'durations_relaxation_fraction':durations_relaxation_fraction_byterm[SEARCHTERMS[idx]],
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
# Create aligned plots, in two panels
# ----> CURRENTLY NOT USED, YOU CAN SKIP THIS <-----
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














