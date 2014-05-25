# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:31:48 2014

@author: admin
"""
import dsift,sift
import numpy as np
from PIL import Image
from pylab import *


dsift.process_image_dsift('empire.jpg','empire.sift',90,40,True)
l,d=sift.read_features_from_file('empire.sift')
im=np.array(Image.open('empire.jpg'))
sift.plot_features(im,l,True)
show()


####################################################################