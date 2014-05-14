# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:41:14 2014

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
#process images at fixed size (50,50)
#for filename in imlist_train:
#    featfile = filename[:-3]+'dsift'
#    dsift.process_image_dsift(filename,featfile,10,5,resize=(50,50))
#for filename in imlist_test:
#    featfile = filename[:-3]+'dsift'
#    dsift.process_image_dsift(filename,featfile,10,5,resize=(50,50))
#



#l,d=sift.read_features_from_file('empire.sift')
#im=np.array(Image.open('empire.jpg'))
#sift.plot_features(im,l,True)
#show()

features,labels = file_tools.read_gesture_features_labels('data/input/train/')
test_features,test_labels = file_tools.read_gesture_features_labels('data/input/test/')
classnames = unique(labels)

# test knn
k = 1
knn_classifier = knn.KnnClassifier(labels,features)
res = array([knn_classifier.classify(test_features[i],k) for i in range(len(test_labels))])


# accuracy
acc = sum(1.0*(res==test_labels))/len(test_labels)
print 'Accuracy:', acc

file_tools.print_confusion(res,test_labels,classnames)


#for the gesture recognition case

import pca
import bayes
V,S,m = pca.pca(features)
V = V[:50]
features=np.array([np.dot(V,f-m) for f in features])
test_features=np.array([np.dot(V,f-m) for f in test_features])
bc = bayes.BayesClassifier()
blist = [features[where(labels==c)[0]] for c in classnames]
bc.train(blist,classnames)
res = bc.classify(test_features)[0]
acc = sum(1.0*(res==test_labels))/len(test_labels)
print 'Accuracy',acc

file_tools.print_confusion(res,test_labels,classnames)

