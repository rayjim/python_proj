# -*- coding: utf-8 -*-
"""
Created on Mon May 26 07:43:12 2014

@author: admin
"""

import sift
import numpy as np
from PIL import Image
from pylab import *

imname ='shape.jpg'
im1=np.array(Image.open(imname).convert('L'))
imname_out = imname[-4]+'.sift'
sift.process_image(imname,imname_out)
l1,d1 = sift.read_features_from_file(imname_out)
figure()
gray()
sift.plot_features(im1,l1,circle=True)
show()