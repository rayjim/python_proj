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
for url in imurls:
    image = urllib.URLopener()
    image.retrieve(url,os.path.basename(urlparse.urlparse(url).path))
    print 'download:', url
    
#######################################################
import sift

nbr_images = len(imlist)

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
# to be constructed
        
        