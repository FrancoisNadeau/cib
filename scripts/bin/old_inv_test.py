#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:57:38 2020

@author: francois
"""
from collections import Counter
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
import numpy as np
import pandas as pd
from taskfunctions import clean_imname
from taskfunctions import flatten
from taskfunctions import get_datas
from taskfunctions import get_synsets

class ImageBank():
    ''' Courtois-Neuromod Image Bank
    '''
    def __init__(self):
        self.syns = get_synsets()
        self.datas = get_datas('../images')
        self.images = self.get_images()
        self.folders = self.get_folders()
        self.im_vectors = self.get_im_vecs()
        self.categories = self.get_categories()
        self.word_freqs = self.get_word_freqs()

    def get_categories(self):
        ''' Description
            -----------
            Gathers each item in self.datas belonging to each category.\
            Would be another part of the pd.MultiIndex.\
            Imported Method(s)
            ------------------
            get_syns()
            Variables
            ---------
            syns: see help(get_syns)
            Returns
            -------
            ImageBank.categories:\
                dict object\
                    keys = categories\
                    values = DF containing each image_concept\
                             in self.datas belonging to each category (key)
        '''
        categories = dict(((syn[0], pd.DataFrame.from_dict(\
                                    dict((row for row in pd.concat([self.images,
                                                                    self.folders]).iterrows()
                                          if syn[0] in row[1]['tags'])),
                                    orient='index'))
                           for syn in self.syns.iterrows()))
        return categories

    def get_word_freqs(self):
        ''' Description
            -----------
            Returns a Counter object counting how often each synset appears\
            in the database, either as image, category, tag, subordinate.
        '''
        return Counter(flatten(self.datas.freq_tags))

    def get_folders(self):
        ''' Description
            -----------
        '''
        folders = pd.DataFrame((row[1]for row in self.datas.iterrows()
                               if not all(pd.isnull(row[1]['subordinates']))),
                              columns=list(self.datas.columns))
        folders['names'] = [bname(folders.loc[ind]['path'])
                           for ind in folders.index]
        folders = folders.set_index('names')
        return folders

    def get_images(self):
        ''' Description
            -----------
            DF containing each image_concept\
            Returns
            -------
            ImageBank.images
        '''
        images = pd.DataFrame((row[1]for row in self.datas.iterrows()
                               if pd.isnull(row[1]['subordinates']).all()),
                              columns=list(self.datas.columns))
        images['names'] = [join(bname(impath), bname(dname(impath)))
                            for impath in images.path]
        images = images.set_index('names')
        return images

    def get_im_vecs(self):
        '''Description
           -----------
           DF containing a an array indexing each image_concept in CNIB\
           with values being either\
               0 :image_concept not in category\
               1 :image_concept in category\
           Returns
           -------
           "Potentially a great pd.MultiIndex?, to be implemented...
           Not very useful at the moment."
           '''
        return pd.DataFrame(np.array([[int(im_tags.__contains__(tag))
                                       for tag in self.syns.index]
                                      for im_tags in self.datas['tags']]),
                            columns=self.syns.index, index=self.datas.index)

CNIB = ImageBank()
DATAS = CNIB.datas
IMAGES = CNIB.images
FOLDERS = CNIB.folders
CATEGORIES = CNIB.categories
SYNS = get_synsets()
IM_VECTORS = CNIB.get_im_vecs()
WORD_FREQS = CNIB.word_freqs
#categories = CATEGORIES
#datas = DATAS
#images = IMAGES
#folders = FOLDERS
#syns = SYNS
#im_vectors = CNIB.get_im_vecs()