#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:43:09 2020

@author: francois
"""

import matplotlib.pyplot as plt 
import os
from os.path import join
from os.path import basename as bname
from os.path import dirname as dname
from os.path import splitext
from nltk.corpus import wordnet as wn  #Import wordnet from the NLTK
import numpy as np
import pandas as pd
from tqdm import tqdm
from taskfunctions import con2syn
from taskfunctions import flatten
from taskfunctions import loadimages
from taskfunctions import splitall
from wordcloud import WordCloud as wc
from wordcloud import STOPWORDS

class cnib():
    def __init__(self):
        self.datas = self.get_data()
#        self.images = self.get_images() 
#        self.categories = self.get_categs()
#        self.thecloud = self.freqlst()
#        self.mat = self.rsa
    def get_data(self):
        fpaths = pd.DataFrame(sorted(list(os.walk('../images')))[1:],
                              columns=['path', 'subordinates', 'concepts'])
        fpaths['tags'] = [splitall(fpath.split('../images')[1])[1:]
                          for fpath in fpaths['path']]
        def get_cnames(fpaths):
            names = []
            for row in fpaths.iterrows():
                if not pd.isnull(row[1]['concepts']).all():
                    if 'object' in row[1]['tags']:
                        names.append(str('_'.join(row[1]['tags'][-1:])))
                    elif 'animal' in row[1]['tags']:
                        names.append(str('_'.join(row[1]['tags'][-2:])))
                    elif 'human' in row[1]['tags']:
                        names.append(str('_'.join(reversed(row[1]['tags'][-3:]))))
                else:
                    names.append(bname(row[1]['path']))
            return names

        fpaths['name'] = get_cnames(fpaths)                              
        fpaths['n_items'] = [len(os.listdir(path))
                             for path in fpaths['path']]
        return fpaths.set_index('name')