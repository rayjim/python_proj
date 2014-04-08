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

#loadsomeimages
im1=array(Image.open('images/001.jpg'))
im2=array(Image.open('images/002.jpg'))

#load2Dpointsforeachviewtoalist
points2D=[loadtxt('2D/00'+str(i+1)+'.corners').T for i in range(3)]
#load3Dpoints
points3D=loadtxt('3D/p3d').T
#loadcorrespondences
corr=genfromtxt('2D/nview-corners',dtype='int',missing='*')
#loadcamerastoalistofCameraobjects
P=[camera.Camera(loadtxt('2D/00'+str(i+1)+'.P')) for i in range(3)]
