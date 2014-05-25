# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 18:11:02 2014

@author: ray
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2*np.pi,num=100)
plt.ion()
for i in xrange(x.size):
    plt.plot(x[:i], np.sin(x[:i]))
    plt.xlim(0,2*np.pi)
    plt.ylim(-1,1)
    plt.draw()
    #plt.clf()