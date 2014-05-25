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
im0 = np.array(Image.open(imname).convert('L')).astype('float')
width = 500
height = 420
im0 = ndimage.zoom(im0,0.9,order = 0)
P_true = np.array([[1.6,0.1,10],[0.4,0.6,0]])
im2 = ndimage.affine_transform(im0,P_true[:2,:2],(P_true[0,2],P_true[1,2]))
im1 = im0
#im2 = np.array(Image.open(imname).convert('L')).astype('float')
#im2 = im1
#im1_gradx = ndimage.sobel(im1,axis=0,mode='constant')
im1_gradx, im1_grady = np.gradient(im1)
#im1_grady = ndimage.sobel(im1,axis=1,mode='constant')
mx=array([[-1,0,1],[-1,0,1],[-1,0,1]])
my=array([[-1,-1,-1],[0,0,0],[1,1,1]])
#im1_gradx = ndimage.convolve(im1,mx)
#im1_grady = ndimage.convolve(im1,my)
gray()
MAXITERS =5000
#P = np.ones((1,6))
#P=np.ones((2,3))
P = np.array([[1,0.1,1],[0.1,1.1,0]])#np.array([[1,0,0],[0,1,0]])
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
def imshow_grad(im):
    """show gradient image by change the dynamic ranges"""
    imshow((im+255)/2)
close('all')
p_val = []

#plt.xlim([0,MAXITERS])
ALPHA = 0.01 # parameters for 
BETA = 0.5
 #step1: Warp image1
im_W = ndimage.affine_transform(im1,P[:2,:2],(P[0,2],P[1,2]))
    #print np.linalg.norm(im_W)
    #step2: compute the error image
im_E = (im2 - im_W.astype('float')).flatten()
for iter in range(MAXITERS):
    # form image 
    
    if (np.linalg.norm(sd)<10e-3):
        print "over at ",iter,"iterations"
        
        break;
   
    #step3: Warp the gradiant
    imx_W = ndimage.affine_transform(im1_gradx,P[:2,:2],(P[0,2],P[1,2]))
    imy_W = ndimage.affine_transform(im1_grady,P[:2,:2],(P[0,2],P[1,2]))
    #im_W = np.vstack((imx_W.flatten(),imy_W.flatten()))
    res = []
    test = []
    #step 4 and 5
    for i in range(im1.shape[0]):
        for j in range(im1.shape[1]):
            res.append(np.dot(np.array([imx_W[i,j],imy_W[i,j]]),p_jacob(i,j)))
           
    sd = np.array(res)
    ta = np.array(test)
    #hessian
    #step6
    H = np.dot(sd.T,sd)
    #step7
    d = np.dot(sd.T,(im_E))
    #step 8
    delta = np.linalg.solve(H,d)
    P_delta = (P.T.flatten()+delta).reshape(3,2).T
    #print np.linalg.norm(delta)
    im_Wnew = ndimage.affine_transform(im1,P_delta[:2,:2],(P_delta[0,2],P_delta[1,2]))
    im_Enew = (im2 -im_Wnew).flatten()
    t = 1
    
    while np.dot(im_Enew.T,im_Enew)>np.dot(im_E.T,im_E)+np.dot(sd.T,np.dot(sd,delta))*ALPHA*t:
        t = t*BETA
        print 't = ', t
        t_delta = t*delta
        P_delta = (P.T.flatten()+t_delta).reshape(3,2).T
        im_Wnew = ndimage.affine_transform(im1,P_delta[:2,:2],(P_delta[0,2],P_delta[1,2]))
        im_Enew = (im2 -im_Wnew).flatten()
   # plot(iter,np.linalg.norm(delta),'bo')
    #plt.draw()
    #plt.clf()
    print 't = ', t
   #print np.linalg.norm(delta)
    p_val.append(np.linalg.norm(delta))
    im_E = im_Enew.copy()
   
    #p_val.append(delta)
    #delta.reshape(3.2).T
    print np.linalg.norm(sd)
   # P = (P.T.flatten()+delta*t).reshape(3,2).T
    P = P_delta.copy()



imshow(im_E.reshape(im1.shape))
figure()
plt.plot(range(size(p_val)),np.abs(p_val),'b-')



