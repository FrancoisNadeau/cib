#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 04:59:46 2020

@author: francois
"""

import os
from os.path import basename as bname
from os.path import dirname as dname
import numpy as np
import pandas as pd
from tqdm import tqdm
from taskfunctions import flatten
from taskfunctions import loadimages
from taskfunctions import splitall

class im10k():
    '''Generates im10k (pandas Dataframe)\n
       rows = im_names\n
       cols= ['im_name', 'n_pic', 'dir', 'tags', 'vec']\n
       Parameter(s)\n
       ------------\n
       'imdir': top image folder ('images' in cnib)\n
       Variables\n
       ---------\n
       'impaths': list of all image paths (see 'taskfunctions.py')\n
       'im_names': list of all im_names, quantity of images in folder,\
                             folders paths\n
           i.e. 'body_part_dog_tail', 'body_beaver', 'face_bveaver',
                'shoe', 'male_teen' etc.
       'all_tags': ordered list of all possible unique tags\n
       'im10k': conversion of im_names to DF.
                   im10k['tags'].items()
       'matrix': numpy array of category membership for all images
                 For each image, category membership is represented by 1 or 0
                 (1=Category name in path parts; else 0)
       'imdf': conversion from array to DataFrame to create vectors (as rows)\
               for each image\n
       Returns\n
       -------
       'cnib'\n
       *new columns added during execution:\n
           'tags': lists all folders' names (categories) in imdir\n
            'vec': tuple where each boolean value represents\
            category membership\n
            *categories are ordered as 'all_tags'\n
        DATA ACCESS\n
            cnib.loc['concept_name']['datas']['npic', 'dir', 'tags', 'vec']
    '''
    def __init__(self):
        self.imdir = '../images'
        self.data = self.get_data()
    def get_data(self):
        impaths = loadimages(self.imdir)
        im_names = []
        for impath in impaths:
            if 'object' in impath:
                name = bname(dname(impath))
            else:
                name = bname(dname(impath))+' '+\
                                            bname(dname(dname(impath)))
            if '_' in name:
                name = name.replace('_', ' ')
            im_names.append((name, len(os.listdir(dname(impath))),
                             dname(impath)))
        im_names = sorted(list(dict.fromkeys(list(im_names))))
        im10k = pd.DataFrame(im_names, columns=['im_name', 'n_pic', 'dir'])
        im10k.index = im10k.im_name
        im10k['tags'] = [splitall(folderpath[1].split(self.imdir,
                                                      maxsplit=1)[1])[1:]
                         for folderpath in im10k['dir'].items()]
        self.alltags = sorted(list(dict.fromkeys(flatten(im10k['tags']))))
        matrix = np.array([[bool(tags[1].__contains__(tag))
                            for tag in self.alltags]
                           for tags in im10k['tags'].items()])
        imdf = pd.DataFrame(matrix, index=im10k['im_name'],
                            columns=self.alltags)
        im10k['vec'] = list(row[1] for row in imdf.iterrows())
        im10k = im10k.drop(columns='im_name')
        return im10k
    def categories(self, kword):
        '''Categorizes the DF according to neuromod categories using "tags"'''
        return pd.DataFrame([self.data.loc[row[0]]
                             for row in self.data.iterrows()
                             if kword in self.data.loc[row[0]].tags])
    def categorize(self):
        for tag in tqdm(list(self.data.index)):
            self.tag = self.categories(tag)                
#        self.full_data = pd.DataFrame(zip(self.alltags, list(self.categories(self.data, ind)
#                                              for ind in tqdm(self.alltags))),
#                            index=self.alltags, columns=['categories', 'data']).drop(columns=['categories'])
    

#cnib = im10k_data(imdir)
#example
#aquatic_mammal = cnib.loc['aquatic_mammal']['data']