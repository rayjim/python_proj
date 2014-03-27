# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:02:49 2014
This is the piecewise affine warping

@author: bao
"""

import matplotlib.delaunay as md
import numpy as np
from pylab import *

x,y = np.array(np.random.standard_normal((2,100))) 
centers, edges, tri, neighbors = md.delaunay(x,y)

figure()

for t in tri:
    t_ext = [t[0], t[1],t[2], t[0]] # add first point to end
    plot(x[t_ext],y[t_ext],'r')
    
plot (x,y,'+')
axis('off')
show()