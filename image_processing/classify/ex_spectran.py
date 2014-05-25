# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 22:57:50 2014

@author: ray
"""

import imtools
from PIL import Image 
import pca
from numpy import *
close('all')
# generate data
imlist = imtools.get_imlist('../data/a_selected_thumbs/') 
imnbr = len(imlist)
immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')
V,S,immean = pca.pca(immatrix)
immean = immean.flatten()
projected = array([dot(V[0:40],immatrix[i]-immean) for i in range(imnbr)])

from scipy.cluster.vq import * 


n = len(projected)
# compute distance matrix
S = array([[ sqrt(sum((projected[i]-projected[j])**2)) for i in range(n) ] for j in range(n)], 'f')
# create Laplacian matrix
rowsum = sum(S,axis=0)
D = diag(1 / sqrt(rowsum))
I = identity(n)
L = I - dot(D,dot(S,D))
# compute eigenvectors of L
U,sigma,V = linalg.svd(L)
k=5
# create feature vector from k first eigenvectors # by stacking eigenvectors as columns
features = array(V[:k]).T
# k-means
features = whiten(features)
centroids,distortion = kmeans(features,k)
code,distance = vq(features,centroids)
# plot clusters
for c in range(k):
    ind = where(code==c)[0]
    figure()
    for i in range(minimum(len(ind),39)):
            im = Image.open(imlist[ind[i]])
            subplot(4,10,i+1)
            imshow(array(im))
            axis('equal')
            axis('off')
show()
