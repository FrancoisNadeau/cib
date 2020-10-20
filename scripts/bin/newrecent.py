#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 06:53:47 2020

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
        self.images = self.get_images() 
        self.categories = self.get_categs()
#        self.thecloud = self.freqlst()
#        self.mat = self.rsa
    def get_data(self):
        fpaths = pd.DataFrame(sorted(list(os.walk('../images')))[1:],
                              columns=['path', 'subordinates', 'concepts'])
        fpaths['tags'] = [splitall(fpath.split('../images')[1])[1:]
                          for fpath in fpaths['path']]
        def get_cnames():
            names = []
            for row in fpaths.iterrows():
                n_tags = fpaths['tags'].values
                if not pd.isnull(row[1]['concepts']).all():
                    if 'object' in n_tags:
                        names.append(str('_'.join(n_tags[-1:])))
                    elif 'animal' in n_tags:
                        names.append(str('_'.join(n_tags[-2:])))
                    elif 'human' in n_tags:
                        names.append(str('_'.join(reversed(n_tags[-3:]))))
                else:
                    names.append(bname(row[1]['path']))
            return names
        fpaths['name'] = get_cnames()                              
        fpaths['n_items'] = [len(os.listdir(path)) for path in fpaths['path']]
        return fpaths
    
        def get_all_names():
            allnames2 = list(dict.fromkeys(flatten(list(fpaths.name))))
            allnamesfull = []
            for name in enumerate(allnames2):
                if ' ' in name[1]:
                    allnamesfull.append(name[1].split(' '))
                else:
                    allnamesfull.append(join(name[1]))

            allnames = list(dict.fromkeys(flatten(allnamesfull)))
            allsynsets = pd.read_excel('/home/francois/Desktop/cnib_06aug2020/docs/all_synsets.xlsx')
            cnib_syns = [cnib_syn for cnib_syn in allsynsets if name in cnib_syn]
            all_our_syns = [wn.synset(name) for name in allnamesfull]
            return fpaths.set_index('name')

    def get_images(self):
        return pd.DataFrame((row[1] for row in self.datas.iterrows()
                             if pd.isnull(row[1]['subordinates']).all()),
                            columns=list(self.datas.columns)).set_index('name')

    def get_categs(self):
        return pd.DataFrame((row[1] for row in self.datas.iterrows()
                             if pd.isnull(row[1]['concepts']).all()),
                            columns=list(self.datas.columns)).set_index('name')

#    def rsa(self):
#        def get_syns(concept):
#            en_names = [syn for syn in list(wn.all_synsets()) if syn.pos() == 'n']
#            im_syns = [self.images.index]
#            if ' ' in concept:
#                clist = flatten(concept.split(' '))
#            else:
#                clist = flatten(list(concept))
#            synlist = [wn.synsets(item, pos='n') for item in clist]
#        sim_mat_wn = np.zeros((len(self.datas),len(self.datas)))
#        matrix = pd.DataFrame([get_syns(ind) for ind in self.datas.index])
#        print(len(ind) for ind in matrix.index)
#        
#        matrix.columns=[matrix.index]
#for j in range(0,len(all_concepts_in_THINGS_clean)):
#    for k in range(0,len(all_concepts_in_THINGS_clean)): 
#        s1 = wn.synset(all_concepts_in_THINGS_clean['Wordnet ID4'].values[j])
#        s2 = wn.synset(all_concepts_in_THINGS_clean['Wordnet ID4'].values[k])
#        sim_mat_wn[j,k] =  wn.wup_similarity(s1, s2)
#        sim_mat_wn[k,j] =  wn.wup_similarity(s1, s2)
#        return matrix
#    def similarity():
#        matrix = pd.DataFrame([get_syns(item) for item in images.index])
#pd.read_excel()
#    def freqlst(self): # how many times is a super-ordinate folder crossed while ascending the database, inspired by step2: top-down validation in Hebart's 2018 paper
#        alltags = flatten([splitall(impath.split('../images')[1])[1:-1]
#                                    for impath in loadimages()])
#        tags = sorted(list(dict.fromkeys(alltags)))
#        return dict([(tag, alltags.count(tag)) for tag in tags
#                    if alltags.count(tag) >= 20])
#        return wc().generate_from_frequencies(dict(\
#                     [(tag, alltags.count(tag)) for tag in tags]))
class cnib2():
    def __init__(self):
        self.data = self.get_data()
        self.images = self.get_imgs() 
        self.categories = self.get_categs()
        
    def get_data(self):
        impaths = sorted(loadimages())
        imdir = '../images'
        im_datas = []
        for allim in os.walk(imdir):
            for folder in allim[1]:
                fpath = join(allim[0], folder)
                im_datas.append((folder, splitall(fpath.split(imdir)[1])[1:],
                              [itname for itname in os.listdir(fpath)],
                              len(os.listdir(fpath)), fpath))
        return pd.DataFrame(sorted([data for data in im_datas]),
                            columns=['name', 'tags', 'subordinates',
                                     'n_items', 'path']).set_index('name')
    def get_imgs(self):
        return pd.DataFrame([row[1].drop(['subordinates'])
                             for row in self.data.iterrows()
                             if '.jpg' in str(row[1].subordinates)])
    def get_categs(self):
        return pd.DataFrame([row[1] for row in list(self.data.iterrows())
                             if '.jpg' not in str(row[1].subordinates)])
    def get_categs2(self):
        return pd.DataFrame((row[1] for row in self.data.iterrows()
                             if pd.isnull(row[1]['subordinates']).all()),
                            columns=list(self.data.columns)).set_index('name')
#    def sortcats(self):
#        (self.images.index)
#        (subords for subords in self.categories['subords'])
    ###########################################################################
    #WN synset-based similarity
    # Bottom-up procedure (from object-concepts to top synset)
#    def wn_syn_similarity(self):
#        synset = wn.synsets("Travel")
#        print('Word and Type : ' + synset[0].name())
#        print('Synonym of Travel is: ' + synset[0].lemmas()[0].name())
#        print('The meaning of the word : ' + synset[0].definition())
#        print('Example of Travel : ' + str(synset[0].examples()))
    
#    plt.imshow(wcloud)    
#    
#    plt.figure(figsize = (8, 8)) 
#    plt.axis("off") 
#    plt.tight_layout(pad = 0)
#    plt.show()
# data from THINGS
#xls = pd.ExcelFile('/home/francois/Desktop/cnib_06aug2020/scripts/CogNeuroModels.xlsx')
#df_things_data = xls.parse('THINGS')
#
## sensory-mootor features
#xls = pd.ExcelFile('/home/francois/Desktop/cnib_06aug2020/scripts/CogNeuroModels.xlsx')
#df_LSN_data = xls.parse('LSN')