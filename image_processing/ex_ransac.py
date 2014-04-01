# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 13:23:21 2014
Works for panaroma
@author: admin
"""
import sift
featname = ['Univ'+str(i+1)+'.sift' for i in range(5)]
imname = ['Univ'+str(i+1)+'.jpg' for i in range(5)]
l = {}
d = {}
for i in range(5):
    sift.process_image(imname[i],featname[i])
    l[i],d[i] = sift.read_features_from_file(featname[i])
    
match = {}
for i in rage(4):
    matches[i] = sift.match(d[i+1],d[i])

