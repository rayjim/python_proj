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
close("all")
im1_name = "Gomamugicha1L_1.jpg"
im2_name = "Gomamugicha1L_2.jpg"
im1_sift = "Gomamugicha1L_1.sift"
im2_sift = "Gomamugicha1L_2.sift"
im1 = np.array(Image.open(im1_name).convert('L'))
im2 = np.array(Image.open(im2_name).convert('L'))
sift.process_image(im1_name,im1_sift)
l1,d1 = sift.read_features_from_file(im1_sift)
sift.process_image(im2_name,im2_sift)
l2,d2 = sift.read_features_from_file(im2_sift)
figure()
gray()
subplot(221)
sift.plot_features(im1,l1,circle=True)
subplot(222)
sift.plot_features(im2,l2,circle=True)
show()


#########################
figure()



print 'strarting matching'
matches = imtools.match_twosided(d1,d2)

gray()
imtools.plot_matches(im1,im2,l1, l2, matches[:100])
show()
