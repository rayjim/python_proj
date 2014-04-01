# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 13:23:21 2014
Works for panaroma
@author: admin
"""
import sift
import homography

featname = ['Univ'+str(i+1)+'.sift' for i in range(5)]
imname = ['Univ'+str(i+1)+'.jpg' for i in range(5)]
l = {}
d = {}
for i in range(5):
    sift.process_image(imname[i],featname[i])
    l[i],d[i] = sift.read_features_from_file(featname[i])
    
matches = {}
for i in range(4):
    matches[i] = sift.match(d[i+1],d[i])

# function to convert the matches to hom.points
def convert_points(j):
    ndx = matches[j].nonzero()[0]
    fp = homography.make_homog(l[j+1][ndx,:2].T)
    ndx2 = [int(matches[j][i]) for i in ndx]
    tp = homography.make_homog(l[j][ndx2,:2].T)
    return fp,tp
# estimate homography
    model = homography.RansacModel()
    fp,tp= convert_points(l)
    H_12 = homography.H_from_ransac(fp,tp,model)[0] # im 1 to 2