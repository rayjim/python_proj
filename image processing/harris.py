# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 16:22:41 2014
Harrris corner
@author: ray
"""
from PIL import Image
import numpy as np
import imtools
im = np.array(Image.open('lena.png').convert('L'))
harrisim = imtools.compute_harris_response(im)
filtered_coords = imtools.get_harris_points(harrisim,6,threshold = 0.05)
imtools.plot_harris_points(im, filtered_coords)

