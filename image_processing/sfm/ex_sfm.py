# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 11:07:08 2014

@author: admin
"""

import sfm 
from PIL import Image
import numpy as np
from pylab import *
close('all')
execfile('load_vggdata.py')
#index for points in first two views
ndx=(corr[:,0]>=0)&(corr[:,1]>=0)
#get coordinates and make homogeneous
x1=points2D[0][:,corr[ndx,0]]
x1=vstack((x1,ones(x1.shape[1])) )
x2=points2D[1][:,corr[ndx,1]]
x2=vstack((x2,ones(x2.shape[1])) )
#computeF
F=sfm.compute_fundamental(x1,x2)
#computetheepipole
e=sfm.compute_epipole(F)
#plotting
figure()

imshow(im1)
#ploteachlineindividually,thisgivesnicecolors
for i in range(5):
    sfm.plot_epipolar_line(im1,F,x2[:,i],e,False)
axis('off')
figure()
imshow(im2)
#ploteachpointindividually,thisgivessamecolorsasthelines
for i in range(5):
    plot(x2[0,i],x2[1,i],'o')
axis('off')
show()