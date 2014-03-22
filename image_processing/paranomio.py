# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 10:07:05 2014
This is an exaple in chapter 2.3
@author: bao
"""
import os
import json
import urllib,urlparse

# query for images
url = 'http://www.panoramio.com/map/get_panoramas.php?order=popularity&\
set=public&from=0&to=20&minx=-77.037564&miny=38.896662&\
maxx=-77.035564&maxy=38.898662&size=medium'

c = urllib.urlopen(url)

# get the urls of individual images from JSON

j = json.loads(c.read())
imurls = []
for im in j['photos']:
    imurls.append(im['photo_file_url'])
    
#download image
imlist = []

imgfolder ="wh"
if not os.path.exists(imgfolder):
    os.mkdir(imgfolder)
for url in imurls:
    image = urllib.URLopener()
    file_name = imgfolder+'/'+os.path.basename(urlparse.urlparse(url).path)
    image.retrieve(url,file_name)
    imlist.append(file_name)
    print 'download:', url
    
#######################################################
import sift
nbr_images = len(imlist)
featlist = []
for i in range(nbr_images):
    featfile = os.path.splitext(imlist[i])[0]+'.sift'
    print 'generating features for: ',imlist[i]
    sift.process_image(imlist[i],featfile)
    featlist.append(featfile)



######################################################


matchscores = zeros((nbr_images,nbr_images))
for i in range(nbr_images):
    for j in range(i,nbr_images): # only compute upper triangle
        print 'comparing', imlist[i],imlist[j]
        
        l1,d1 = sift.read_features_from_file(featlist[i])
        l2,d2 = sift.read_features_from_file(featlist[j])
        
        matches = sift.match_twosided(d1,d2)
        
        nbr_matches = sum(matches>0)
        print 'number of matches = ', nbr_matches
        matchscores[i,j] = nbr_matches
        
# copy values
        
for i in range(nbr_images):
    for j in range(i+1,nbr_images):
        matchscores[j,i] = matchscores[i,j]
        
##############################################################
import pydot
from PIL import Image

threshold = 2

g = pydot.Dot(graph_type = 'graph')
path = '/Users/ray/Documents/pythonwork/python_proj/image_processing/' 

for i in range(nbr_images):
    for j in range(i+1,nbr_images):
        if matchscores[i,j] > threshold:
            #first image in pair
            im = Image.open(imlist[i])
            im.thumbnail((100,100))
            filename = str(i)+'.png'
            im.save(filename) # need temporary files of the right size
            g.add_node(pydot.Node(str(i),fontcolor='transparent',shape='rectangle',image = path+filename))
            
            #second image in pair
            im = Image.open(imlist[j])
            im.thumbnail((100,100))
            filename = str(j)+'.png'
            im.save(filename) # need temporary files of the right size
            g.add_node(pydot.Node(str(j),fontcolor='transparent',shape='rectangle',image = path+filename))
            g.add_edge(pydot.Edge(str(i),str(j)))
            
g.write_png('whitehouse.png')
        