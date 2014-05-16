# -*- coding: utf-8 -*-
"""
Created on Fri May 16 15:15:06 2014

@author: admin
"""

import ncut
from scipy.misc import imresize
from numpy import *

close('all')
im=array(Image.open('empire.jpg'))
m,n=im.shape[:2]
#resizeimageto(wid,wid)
wid=50
rim=imresize(im,(wid,wid),interp='bilinear')
rim=array(rim,'f')
#createnormalizedcutmatrix
A=ncut.ncut_graph_matrix(rim,sigma_d=1,sigma_g=1e-2)
#cluster
code,V=ncut.cluster(A,k=3,ndim=3)
#reshapetooriginalimagesize
codeim=imresize(code.reshape(wid,wid),(m,n),interp='nearest')
#plotresult
figure()
imshow(codeim)
gray()
show()