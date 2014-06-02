# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:57:47 2014

@author: admin
"""
import matplotlib.tri as tri
from matplotlib.mlab import griddata
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import os
import calc_tsne as tsne
plt.close('all')
path = 'data_3'
imlist =[os.path.join(path,f) for f in os.listdir(path) if f.endswith('.out')]
#for filename in imlist:
#    kp=np.loadtxt(filename) #read all keypoint
#    c_x = kp[:,0]
#    c_y = kp[:,1]
#    scale = kp[:,2]
#    ori = kp[:,3]
#    plt.figure(1)
#    y, binEdges = np.histogram(scale,bins=100)
#    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
#    plt.plot(bincenters,y)
#    plt.figure(2)
#    y, binEdges = np.histogram(ori,bins=100)
#    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
#    plt.plot(bincenters,y)

kp=np.loadtxt(imlist[6]) #read all keypoint
c_x = kp[:,0]
c_y = kp[:,1]
scale = kp[:,2]
ori = kp[:,3]
plt.figure(1)
y, binEdges = np.histogram(scale,bins=100)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
plt.plot(bincenters,y)
plt.figure(2)
y, binEdges = np.histogram(ori,bins=100)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
plt.plot(bincenters,y)
plt.figure(1)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)   
plt.title('Scale')
plt.figure(2)
plt.title('ori')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)    
       

















###############################################
#filename = imlist[2]
#
#fig=plt.figure()
#kp=np.loadtxt(filename) #read all keypoint
#x=kp[:,0]
#y=kp[:,1]
#z=np.log(kp[:,2])*1000 #scale
#c=np.degrees(kp[:,3]) #ori
#width = kp[0,4]
#height= kp[0,5]
#
############plot############################
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(x,y,z,s=z,c=c,cmap=plt.hot())
#
#plt.show() 
#figure()
#scatter(x,y,cmap=plt.hot())
#y, binEdges = np.histogram(z,bins=100)
#bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
