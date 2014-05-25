# -*- coding: utf-8 -*-
"""
Created on Thu May 15 07:26:36 2014

@author: admin
"""


import dsift,sift
import numpy as np
from PIL import Image
from pylab import *
import os
import file_tools
import knn

path_train = 'data/input/train/'
path_test = 'data/input/test/'
imlist_train = [os.path.join(path_train,f) for f in os.listdir(path_train) if f.endswith('.ppm')]
imlist_test = [os.path.join(path_test,f) for f in os.listdir(path_test) if f.endswith('.ppm')]
features,labels = file_tools.read_gesture_features_labels('data/input/train/')
test_features,test_labels = file_tools.read_gesture_features_labels('data/input/test/')
classnames = unique(labels)
#for the gesture recognition case

import pca
import bayes
V,S,m = pca.pca(features)
dim = np.arange(10,200,10)
acclist = []
for ii in dim:
    print 'dimension is: ',ii
    V_s = V[:ii]
    features_s=np.array([np.dot(V_s,f-m) for f in features]) #train
    test_features_s=np.array([np.dot(V_s,f-m) for f in test_features]) #test
    bc = bayes.BayesClassifier()
    blist = [features_s[where(labels==c)[0]] for c in classnames]
    bc.train(blist,classnames)
    res = bc.classify(test_features_s)[0]
    acc = sum(1.0*(res==test_labels))/len(test_labels)
    print acc
    acclist.append(acc)
    
plot(dim,acclist,'b+-')





