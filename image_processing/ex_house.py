# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 20:23:34 2014

@author: ray
"""

import camera
import numpy as np
import pylab

#load points
points = loadtxt('data/house.p3d').T
points = np.vstack((points,np.ones(points.shape[1])))


P = np.hstack((np.eye(3),np.array([[0],[0],[-10]])))
cam = camera.Camera(P)
x = cam.project(points)

# plot projection
figure()
plot(x[0],x[1],'k.')
show()

r = 0.05*np.random.rand(3)
rot = camera.rotation_matrix(r)

figure()
for t in range(20):
    cam.P = np.dot(cam.P,rot)
    x = cam.project(points)
    plot(x[0],x[1],'k')
show()