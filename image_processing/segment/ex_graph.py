# -*- coding: utf-8 -*-
"""
Created on Fri May 16 09:22:20 2014

@author: admin
"""
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow

gr=digraph()
gr.add_nodes([0,1,2,3])

gr.add_edge((0,1), wt=4)
gr.add_edge((1,2), wt=3)
gr.add_edge((2,3), wt=5)
gr.add_edge((0,2), wt=3)
gr.add_edge((1,3), wt=4)
flows,cuts=maximum_flow(gr,0,3)
print 'flowis:',flows
print 'cutis:',cuts

print
from scipy.misc import imresize
import graphcut
from pylab import *
from PIL import Image

im=array(Image.open('empire.jpg'))
im=imresize(im,0.07,interp='bilinear')
size=im.shape[:2]
#addtworectangulartrainingregions
labels=zeros(size)
labels[3:18,3:18]=-1
labels[-18:-3,-18:-3]=1
#creategraph
gg=graphcut.build_bayes_graph(im,labels,kappa=1)
#cutthegraph
print 'cutting graph...'
res=graphcut.cut_graph(gg,size)
print 'finishing cutting'
figure()
graphcut.show_labeling(im,labels)
figure()
imshow(res)
gray()
axis('off')
show()