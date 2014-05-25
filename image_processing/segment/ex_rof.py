# -*- coding: utf-8 -*-
"""
Created on Fri May 16 15:37:09 2014

@author: admin
"""

import rof
from numpy import *

im=array(Image.open('empire.jpg').convert('L'))
U,T=rof.denoise(im,im,tolerance=0.001)
t=0.4#threshold
import scipy.misc
scipy.misc.imsave('result.pdf',U<t*U.max())