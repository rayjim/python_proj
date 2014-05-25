# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:39:22 2014

@author: admin
"""
import imtools
import numpy as np
from PIL import *
import os 
from scipy.misc import imresize

def compute_feature(im):
    """return a feature vector for an ocr image patches"""
    
    #resize and remove border
    norm_im = imresize(im,(30,30))
    norm_im = norm_im[3:-3,3:-3]
    
    return norm_im.flatten()
    
def load_ocr_data(path):
    """ Retrun labels and ocr features for all images in path"""
    #create list of all files ending in .jpg
    imlist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
    #create labels
    labels=[int(imfile.split('/')[-1][0]) for imfile in imlist]
    
    #create featuers from the images
    features =[]
    for imname in imlist:
        im=np.array(Image.open(imname).convert('L'))
        features.append(compute_feature(im))
    return np.array(features), labels
    
from scipy.ndimage import measurements

def find_sudoku_edges(im,axis=0):
    """Finds thecelledgesforanalignedsudokuimage."""
    #threshold and sum rows and columns
    trim=1*(im<128)
    s=trim.sum(axis=axis)
    #find center of stronges tlines
    s_labels,s_nbr=measurements.label(s>(0.5*max(s)))
    m=measurements.center_of_mass(s,s_labels,range(1,s_nbr+1))
    x=[int(x[0]) for x in m]
    #if only the strong lines are detected add lines in between
    if len(x)==4:
        dx=np.diff(x)
        x=[x[0],x[0]+dx[0]/3,x[0]+2*dx[0]/3,
            x[1],x[1]+dx[1]/3,x[1]+2*dx[1]/3,
            x[2],x[2]+dx[2]/3,x[2]+2*dx[2]/3,x[3]]
    if len(x)==10:
        return x
    else:
        raise RuntimeError('Edges not detected.')
