# -*- coding: utf-8 -*-
"""
Created on Wed May 14 15:11:50 2014

@author: admin
"""

import sift
from PIL import Image
import numpy as np
from pylab import *
import os
from pylab import *

def process_image_dsift(imagename,resultname,size=20,steps=10,
                        force_orientation=False,resize=None):
    """Process an image with densely sampled SIFT descriptors
    and savethe results in a file.Optional input:size of features,
    steps between locations,forcing computation of descriptor orientation
    (False means all are oriented upwards),tuple for resizing the image."""
    im=Image.open(imagename).convert('L')
    if resize!=None:
        im=im.resize(resize)
    m,n=im.size
    if imagename[-3:]!='pgm':
        #create a pgm file
        im.save('tmp.pgm')
        imagename='tmp.pgm'
    #createframesandsavetotemporaryfile
    scale=size/3.0
    x,y=meshgrid(range(steps,m,steps),range(steps,n,steps))
    xx,yy=x.flatten(),y.flatten()
    frame=np.array([xx,yy,scale*ones(xx.shape[0]),zeros(xx.shape[0])])
    savetxt('tmp.frame',frame.T,fmt='%03.3f')
    if force_orientation:
        cmmd=str("sift "+imagename+" --output="+resultname+
            " --read-frames=tmp.frame --orientations")
    else:
        cmmd=str("sift "+imagename+" --output="+resultname+
        " --read-frames=tmp.frame")
    os.system(cmmd)
    print 'processed',imagename,'to',resultname