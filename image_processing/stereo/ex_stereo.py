# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 20:16:31 2014

@author: ray
"""
import stereo
import numpy as np
from PIL import Image

im_l = np.array(Image.open('scene1.row3.col3.ppm').convert('L'),'f')
im_r = np.array(Image.open('scene1.row3.col4.ppm').convert('L'),'f')
# starting displacement and steps
steps = 12
start = 4
# width for ncc
wid = 9
res = stereo.plane_sweep_ncc(im_l,im_r,start,steps,wid)
import scipy.misc 
scipy.misc.imsave('depth_1.png',res)
res = stereo.plane_sweep_gauss(im_l,im_r,start,steps,wid)
scipy.misc.imsave('depth_2.png',res)