#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:20:50 2023

@author: m.wehrens
"""



###############################################################################

customized_sample_list = [S for S in sample_info_dicts['name'] if 'day1_' in S]

for S_IDX in range(len(customized_sample_list)):
    
    # S_IDX=4
    
    samplename = ['','']
    samplename[0] = customized_sample_list[S_IDX]
    samplename[1] = samplename[0].replace('day1','day2')
    
    F, axs = plt.subplots(1, 2)
    for S_IDX_sub in [0,1]:
        
        # Load the image
        img = mpimg.imread(my_work_dir+samplename[S_IDX_sub]+'/'+samplename[S_IDX_sub]+\
                            '_t'+str(img_idx).zfill(4)+IMGNAMESUFFIX+'.tif')
        # img = img[:,:,0] # depends how images where exported        
        img_norm = (img-np.min(img))/(np.max(img)-np.min(img))
        
        # What are the ROI coordinates?
        current_roi = sample_info_dicts['roi'][samplename[S_IDX_sub]]
        
        # Plot it
        # using the variable ax for single a Axes

        
        # using the variable axs for multiple Axes
        
        axs[S_IDX_sub].imshow(img_norm[current_roi[0]:current_roi[1],current_roi[2]:current_roi[3]], cmap = 'gray')    
        axs[S_IDX_sub].set_title(samplename[S_IDX_sub])

        
           
    
    # plt.show()    
    plt.savefig(ROI_dir+'COMPARISON_ROI_'+samplename[0]+'_'+samplename[1]+'.pdf')
    plt.close(F)
    