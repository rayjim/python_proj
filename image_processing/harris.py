# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 16:22:41 2014
Harrris corner
@author: ray
"""
from PIL import Image
import numpy as np
import imtools
from pylab import *


im = np.array(Image.open('lena.png').convert('L'))
harrisim = imtools.compute_harris_response(im)
filtered_coords = imtools.get_harris_points(harrisim,6,threshold = 0.05)
imtools.plot_harris_points(im, filtered_coords)


## matching
figure()
wid = 5
im1 = np.array(Image.open('lena.png').convert('L'))
im2 = np.array(Image.open('lena.png').convert('L'))


harrisim = imtools.compute_harris_response(im1,5)
filtered_coords1 = imtools.get_harris_points(harrisim,wid+1)
d1 = imtools.get_descriptors(im1,filtered_coords1,wid)

harrisim = imtools.compute_harris_response(im2,5)
filtered_coords2 = imtools.get_harris_points(harrisim,wid+1)
d2 = imtools.get_descriptors(im2,filtered_coords2,wid)

print 'strarting matching'
matches = imtools.match_twosided(d1,d2)

gray()
imtools.plot_matches(im1,im2,filtered_coords1, filtered_coords2, matches[:100])
show()

