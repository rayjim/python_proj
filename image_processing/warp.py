# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 10:10:32 2014
Warp image
@author: bao
"""
import numpy as np
import homography as hg
from scipy import ndimage

def image_in_image(im1,im2,tp):
    """ Put im1 in im2 with an affine tranformation such that
    corners are as colse to tp as possible
    tp are homogeneous and counter-clockwise from top left"""
    
    # points to warp from
    
    m,n = im1.shape[:2]
    fp = np.array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])
    
    # compute affine transform and apply
    
    H = hg.Haffine_from_points(tp,fp)
    
    im1_t = ndimage.affine_transform(im1,H[:2,:2],(H[0,2],H[1,2]),im2.shape[:2])
    alpha = (im1_t>0)
    return (1-alpha)*im2+alpha*im1_t
    
