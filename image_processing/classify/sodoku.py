# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:39:22 2014

@author: admin
"""
import imtools
import numpy as np
from PIL import *

def compute_feature(im):
    """return a feature vector for an ocr image patches"""
    
    #resize and remove border
    norm_im = imresize(im,(30,30))
    norm_im = norm_im[3:-3,3:-3]
    
    return norm_im.flatten()
    
def load_ocr_data(path):
    