# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 18:05:15 2014
LK 
@author: admin
"""

from PIL import Image
import numpy as np
from pylab import * 
from scipy import ndimage
from scipy.linalg import block_diag

imname = "../lena.png"
im1 = np.array(Image.open(imname).convert('L'))
im2 = np.array(Image.open(imname).convert('L'))
#im1_gradx = ndimage.sobel(im1,axis=0,mode='constant')
#im1_gradx, im1_grady = np.gradient(im1)
#im1_grady = ndimage.sobel(im1,axis=1,mode='constant')
mx=array([[-1,0,1],[-1,0,1],[-1,0,1]])
my=array([[-1,-1,-1],[0,0,0],[1,1,1]])
im1_gradx = ndimage.convolve(im1,mx)
im1_grady = ndimage.convolve(im1,my)
gray()
MAXITERS = 1000
P = np.ones((2,3))*.5
#P=np.zeros((2,3))

def p_jacob(x,y):
    return np.array([[x,0,y,0,1,0],[0,x,0,y,0,1]])
#generate jacobian
#r = np.array([])
#for i in range(im1.shape[0]):
#    for j in range(im1.shape[1]):
#        #create jacob
#        r = block_diag(r,p_jacob(i,j))
#    
e = 10e-5
delta = 500


for iter in range(MAXITERS):
    # form image 
    
    if (np.linalg.norm(delta)<10e-5):
        print "over at ",iter,"iterations"
        
        break;
    #step1: Warp image1
    im_W = ndimage.affine_transform(im1,P[:2,:2],(P[0,2],P[1,2]))
    #step2: compute the error image
    im_E = im2 - im_W
    #step3: Warp the gradiant
    imx_W = ndimage.affine_transform(im1_gradx,P[:2,:2],(P[0,2],P[1,2]))
    imy_W = ndimage.affine_transform(im1_grady,P[:2,:2],(P[0,2],P[1,2]))
    #im_W = np.vstack((imx_W.flatten(),imy_W.flatten()))
    res = []
    #step 4 and 5
    for i in range(im1.shape[0]):
        for j in range(im1.shape[1]):
            res.append(np.dot(np.array([imx_W[i,j],imy_W[i,j]]),p_jacob(i,j)))
    grad = np.array(res)
    #hessian
    #step6
    H = np.dot(grad.T,grad)
    #step7
    d = np.dot(grad.T,(im_E).flatten())
    #step 8
    delta = np.linalg.solve(H,d)
    print np.linalg.norm(delta)
    P = (P.flatten()+delta).reshape(2,3)
imshow(im_E)