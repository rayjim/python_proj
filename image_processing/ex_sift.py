# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 16:50:12 2014
Sift example
@author: ray
"""

import sift
from PIL import Image
import numpy as np
from pylab import *
import imtools

close('all')
imname = 'lena.png'
im1 = np.array(Image.open(imname).convert('L'))
im2 = np.array(Image.open(imname).convert('L'))
sift.process_image(imname,'lena1.sift')
l1,d1 = sift.read_features_from_file('lena1.sift')
figure()
gray()
sift.plot_features(im1,l1,circle=True)
show()


#########################
figure()
sift.process_image(imname,'lena2.sift')
l2,d2 = sift.read_features_from_file('lena2.sift')


print 'strarting matching'
matches = sift.match_twosided(d1,d2)

gray()
imtools.plot_matches(im1,im2,l1, l2, matches)
show()
