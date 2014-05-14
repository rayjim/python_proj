# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:09:29 2014

@author: admin
"""

import os
import sift
import numpy as np

def read_gesture_features_labels(path):
    featlist = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.dsift')]
   # print featlist
    #read the feature
    features = []
    for featfile in featlist:
        l,d = sift.read_features_from_file(featfile)
        features.append(d.flatten())
    features = np.array(features)
    
    #create labels
    labels = [featfile1.split('/')[-1][0] for featfile1 in featlist]
    
    return features,np.array(labels)
    
def print_confusion(res,test_labels,classnames):
    n=len(classnames)
    #confusionmatrix
    class_ind = dict([(classnames[i], i) for i in range(n)])
    confuse=np.zeros((n,n))
    for i in range(len(test_labels)):
        confuse[class_ind[res[i]],class_ind[test_labels[i]]]+=1
    print 'Confusionmatrixfor'
    print classnames
    print confuse
