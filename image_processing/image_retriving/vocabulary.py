# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 02:08:07 2014

@author: ray
"""
from scipy.cluster.vq import * 
import sift as sift
from numpy import *
class Vocabulary(object):
    def __init__(self,name): 
        self.name = name 
        self.voc = []
        self.idf = [] 
        self.trainingdata = []
        self.nbr_words = 0
    def train(self,featurefiles,k=100,subsampling=10):
        """ Train a vocabulary from features in files listed
              in featurefiles using k-means with k number of words.
              Subsampling of training data can be used for speedup. """
        nbr_images = len(featurefiles)
        # read the features from file
        descr = [] 
        descr.append(sift.read_features_from_file(featurefiles[0])[1]) 
        descriptors = descr[0] #stack all features for k-means
        for i in arange(1,nbr_images):
            print 'appending ',featurefiles[i]
            descr.append(sift.read_features_from_file(featurefiles[i])[1]) 
            descriptors = vstack((descriptors,descr[i]))
            # k-means: last number determines number of runs
        print 'k-means processing...'
        self.voc,distortion = kmeans(descriptors[::subsampling,:],k,1) 
        print 'finish k-means'
        self.nbr_words = self.voc.shape[0]
            # go through all training images and project on vocabulary
        imwords = zeros((nbr_images,self.nbr_words)) 
        for i in range( nbr_images ):
              print 'processing ',featurefiles[i]
              imwords[i] = self.project(descr[i])
        nbr_occurences = sum( (imwords > 0)*1 ,axis=0)
        self.idf = log( (1.0*nbr_images) / (1.0*nbr_occurences+1) ) 
        self.trainingdata = featurefiles
    def project(self,descriptors):
        """ Project descriptors on the vocabulary
              to create a histogram of words. """
            # histogram of image words
        imhist = zeros((self.nbr_words)) 
        words,distance = vq(descriptors,self.voc) 
        for w in words:
            imhist[w] += 1 
        return imhist
