# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 18:05:15 2014
LK 
@author: admin
"""

from PIL import Image
import numpy as np
from pylab import * 
from scipy import ndimage

imname = "lena.jpg"
im1 = np.array(Image.open(imname).convert('L'))
im1_gradx = ndimage.sobel(im1,axis=0,mode='constant')
im1_grady = ndimage.sobel(im1,axis=1,mode='constant')
im2 = np.array(Image.open(imname).convert('L'))
MAXITERS = 10000
P = np.zeros((3,2))
def p_jocob(x,y):
    return np.array([x,0,y,0,1,0],[0,x,0,y,0,1])
#generate jacobian


for iter in range(MAXITERS):
    # form image warp
    im_W = ndimage.affine_transform(im1,P[:2,:2],(P[0,2],P[1,2]))
    # compute the error image
    im_E = im2 - im_W
    # Warp the gradiant
    imx_W = ndimage.affine_transform(im1_gradx,P[:2,:2],(P[0,2],P[1,2]))
    imy_W = ndimage.affine_transform(im1_grady,P[:2,:2],(P[0,2],P[1,2]))
    