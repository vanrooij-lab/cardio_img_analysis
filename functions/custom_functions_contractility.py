#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:19:51 2023

@author: m.wehrens
"""

import numpy as np

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


