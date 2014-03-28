# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 03:04:38 2014

@author: ray
"""

from PIL import Image
from scipy import ndimage
import numpy as np
from pylab import *

im = np.array (Image.open('lena.png').convert('L'))
H = array([[1.4,0.05,-100],[0.05,1.5,-100],[0,0,1]])
im2 = ndimage.affine_transform(im,H[:2,:2],(H[0,2],H[1,2]))

figure()
gray()
imshow(im2)
imshow(im2)


# another example

import warp as warp
import homography

# example of affine warp of im1 onto im2

im1 = np.array(Image.open('beatles.jpg').convert('L'))
im2 = np.array(Image.open('billboard_for_rent.jpg').convert('L'))

tp = np.array([[264,538,540,264],[40,36,605,605],[1,1,1,1]])

im3 = warp.image_in_image(im1,im2,tp)

figure()
gray()
imshow(im3)
axis('equal')
axis('off')
show()


#set for points to corners of im1

m,n = im1.shape[:2]
fp = array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])

# first triangle
tp2 = tp[:,:3]
fp2 = fp[:,:3]


# compute H

H = homography.Haffine_from_points(tp2,fp2)
im1_t= ndimage.affine_transform(im1,H[:2,:2],(H[0,2],H[1,2]),im2.shape[:2])

# alpha for triangle
alpha = warp.alpha_for_triangle(tp2,im2.shape[0], im2.shape[1])
im4 = (1-alpha)*im3+alpha*im1_t

figure()
gray()
imshow(im4)
axis('equal')
axis('off')
show()

###############################3

fromim = np.array(Image.open('sunset_tree.jpg'))
x,y = meshgrid(range(5),range(6))
x = (fromim.shape[1]/4)*x.flatten()
y = (fromim.shape[0]/5)*y.flatten()

# triangulate

tri = warp.triangulate_points(x,y)

im = np.array(Image.open('turningtorso1.jpg'))
tp = loadtxt('turningtorso1_points.txt')

# convert points to hom. coordinates

fp = np.vstack((y,x,np.ones((1,len(x)))))
tp = np.vstack((tp[:,1],tp[:,0],ones((1,len(tp)))))

# warp triangles
im = warp.pw_affine(fromim,im,fp,tp,tri)

figure()
imshow(im)
warp.plot_mesh(tp[1],tp[0],tri)
axis('off')
show()
















