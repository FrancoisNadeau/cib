#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:12:06 2020

@author: francois
"""
from collections import Counter
import os
from os.path import basename as bname
from os.path import dirname as dname
from nltk.corpus import wordnet as wn  #Import wordnet from the NLTK
import numpy as np
import pandas as pd
from tqdm import tqdm
from taskfunctions import flatten
from taskfunctions import loadimages
from taskfunctions import splitall
from taskfunctions import clean_imname

class binned_cnib():
    def __init__(self):
        self.all_syns = self.get_all_syns()
        self.images = self.get_images()
        self.distribution = self.get_distribution()
        
    def get_all_syns(self): #contains specific animal body parts
        names2 = sorted(list(dict.fromkeys(list(self.datas.index))))
        full_lst = []
        for name in names2:
            if ' ' in name:
                full_lst.append(list(name.split(' ')))
            else:
                full_lst.append(name)
        return sorted(list(dict.fromkeys(flatten(full_lst))))
    def get_images(self):
        return pd.DataFrame(sorted(list(dict.fromkeys(\
                            [(clean_imname(bname(impath)),
                              len(os.listdir(dname(impath))),
                              splitall(impath.split('../images')[1])[1:-1])
                             for impath in loadimages()]))),
                            columns=['im_name', 'n_items', 
                                     'tags']).set_index('im_name')
    # long to load, maybe not necessary...
    def get_distribution(self):
        distribution = pd.DataFrame([[im[1] for im in self.images.iteritems()
                                          if categ in im[1].tags]
                                          for categ in self.categories],
                                          index=self.categories)
        return distribution