# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 10:06:56 2014

@author: admin
"""

from PIL import Image
import camera
import numpy as np
from pylab import * 
import sfm
close('all')
execfile('load_vggdata.py') 
corr=corr[:,0]#view1
ndx3D=where(corr>=0)[0]#missing values are-1
ndx2D=corr[ndx3D]
#select visible points and makehomogeneous
x=points2D[0][:,ndx2D]#view1
x=vstack((x,ones(x.shape[1])) )
X=points3D[:,ndx3D]
X=vstack((X,ones(X.shape[1])) )
#estimateP
Pest=camera.Camera(sfm.compute_P(x,X))
print "okay1"
#compare!
print Pest.P/Pest.P[2,3]
print P[0].P/P[0].P[2,3]

xest=Pest.project(X)
print"okay2"
#plotting
figure()
imshow(im1)
plot(x[0],x[1],'b.')
plot(xest[0],xest[1],'r.')
axis('off')
show()
