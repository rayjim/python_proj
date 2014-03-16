# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 17:14:50 2014
Sift
@author: ray
"""
###############################################################################
# Sift
import Image
import os
import numpy as np
from pylab import *

def process_image(imagename,resultname,params="--edge-thresh 10 --peak-thresh 5"):
    
    if imagename[-3:]!="pgm":
       #create a pgm file   
       im = Image.open(imagename).convert('L')
       im.save('tmp.pgm')
       imagename ="tmp.pgm"
    
    cmmd = str("./sift "+imagename+" --output "+resultname+" "+params)
    os.system(cmmd)
    print 'processed', imagename, 'to', resultname
    
    
    
def read_features_from_file(filename):
    """ Read feature properties and return in matrix form"""
    
    f = np.loadtxt(filename)
    return f[:,:4],f[:,:4] # feature locations, descriptors
    
def write_features_to_file(filename, locs, desc):
    """Save feature location and descriptor to file"""
    np.savetxt(filename,hstack((locs,desc)))
    
def plot_features(im,locs, circle=False):
    """Show image with features. input: im(image as array)
    locs(row,col,scale,orientation of each feature)."""
    
    def draw_circle(c,r):
        t = arange(0,1.01,.01)*2*pi
        x = r*cos(t)+c[0]
        y = r*sin(t)+c[1]
        plot(x,y,'b',linewidth=2)
        
    imshow(im)
    if circle:
        for p in locs:
            draw_circle(p[:2],p[2])
    else:
            plot(locs[:,0],locs[:,1],'ob') 
    axis('off')

def match(desc1, desc2):
    """ For each descriptor in the first image, 
    select its match in the second image.
    input: desc1
    desc2."""
    
    desc1 = array([d/np.linalg.norm(d) for d in desc1])
    desc2 = array([d/np.linalg.norm(d) for d in desc2])
    
    dist_ratio = 0.6
    desc1_size = desc1.shape
    
    matchscores = zeros((desc1_size[0],1),'int')
    desc2t = desc2.T
    for i in range(desc1_size[0]):
        dotprods = dot(desc1[i,:],desc2t)
        dotprods = 0.9999+dotprods
        #inverse cosine and sort, return index for features in second image
        indx = argsort(arccos(dotprods))
        
        if arccos(dotprods)[indx[0]]<dist_ratio*arccos(dotprods)[indx[1]]:
            matchscores[i] = int(indx[0])
        
    return matchscores
        
        
def match_twosided(desc1, desc2):
    matches_12 = match(desc1,desc2)
    matches_21 = match(desc2,desc1)
    
    ndx_12 = matches_12.nonzero()[0]
    
    for n in ndx_12:
        if matches_21[int(matches_12[n])]!=n:
            matches_12[n] = 0
            
    return matches_12
        
        
        
        
        
        
        
        
        
        
        