# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 02:05:52 2014
visual words example
@author: ray
"""
import os 
import numpy as np
import sift
import imtools
imlist = imtools.get_imlist('ukbench/small/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images)]
#for i in range(nbr_images): 
#    sift.process_image(imlist[i],featlist[i])
import pickle 
import vocabulary
nbr_images = len(imlist)
featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images) ]
voc = vocabulary.Vocabulary('ukbenchtest')
voc.train(featlist,1000,10)
# saving vocabulary
with open('vocabulary.pkl', 'wb') as f:
  pickle.dump(voc,f)
print 'vocabulary is:', voc.name, voc.nbr_words
