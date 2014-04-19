# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 16:56:07 2014

@author: ray
"""

import hcluster
import imtools
from numpy import *
class1 = 1.5*randn(100,2)
class2 = randn(100,2) + array([5,5])
features = vstack((class1,class2))
tree = hcluster.hcluster(features) 
clusters = tree.extract_clusters(5)
print len(clusters) 
for c in clusters:
    print c.get_cluster_elements()
    
import os 
import hcluster
# create a list of images
path = 'flickr-sunsets/'
imlist = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
# extract feature vector (8 bins per color channel)
features = zeros([len(imlist), 512]) 
for i,f in enumerate(imlist):
  im = array(Image.open(f))
  # multi-dimensional histogram
  h,edges = histogramdd(im.reshape(-1,3),8,normed=True,range=[(0,255),(0,255),(0,255)]) 
  features[i] = h.flatten()
  
tree = hcluster.hcluster(features)
hcluster.draw_dendrogram(tree,imlist,filename='sunset.pdf')
# visualize clusters with some (arbitrary) threshold
clusters = tree.extract_clusters(0.23*tree.distance)
# plot images for clusters with more than 3 elements
for c in clusters:
    elements = c.get_cluster_elements() 
    nbr_elements = len(elements)
    if nbr_elements>3:
        figure()
        for p in range(minimum(nbr_elements,20)):
              subplot(4,5,p+1)
              im = array(Image.open(imlist[elements[p]]))
              imshow(im)
              axis('off')
show()
