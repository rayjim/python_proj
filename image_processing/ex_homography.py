# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 03:04:38 2014

@author: ray
"""

from PIL import Image
from scipy import ndimage
import numpy as np
from pylab import *

im = np.array (Image.open('lena.png').convert('L'))
H = array([[1.4,0.05,-100],[0.05,1.5,-100],[0,0,1]])
im2 = ndimage.affine_transform(im,H[:2,:2],(H[0,2],H[1,2]))

figure()
gray()
imshow(im2)
imshow(im2)
