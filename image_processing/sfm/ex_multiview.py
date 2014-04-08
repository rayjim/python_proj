# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 09:37:02 2014
example for sfm
@author: admin
"""
from PIL import Image
import camera
import numpy as np
from pylab import *
close('all')
execfile('load_vggdata.py')
#make3Dpointshomogeneousandproject
X=vstack((points3D,ones(points3D.shape[1])) )
x=P[0].project(X)
#plottingthepointsinview1
figure()
imshow(im1)
plot(points2D[0][0],points2D[0][1],'*')
axis('off')
figure()
imshow(im1)
plot(x[0],x[1],'r.')
axis('off')
show()


from mpl_toolkits.mplot3d import axes3d
fig=figure()
ax=fig.gca(projection="3d")
#generate3Dsampledata
X,Y,Z=axes3d.get_test_data(0.25)
#plotthepointsin3D
ax.plot(X.flatten(),Y.flatten(),Z.flatten(),'o')
show()

fig=figure()
ax=fig.gca(projection='3d')
ax.plot(points3D[0],points3D[1],points3D[2],'k.')