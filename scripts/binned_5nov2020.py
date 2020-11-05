#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:35:19 2020

@author: francois
"""
import json
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from random import sample
from typing import Sequence
import pandas as pd
from nltk.corpus import wordnet as wn
###############################################################################
# Reloaded modules
from taskfunctions import flatten
from taskfunctions import loadimages
###############################################################################

def sampling(lst, nsize, nsamples, exclusives=[]):
    '''
    Description
    -----------
    Draws desired amount of samples of desired size without
    replacement from population.
    Output can be either list or dict.

    Parameters
    ----------
    lst: type=list
        Input list from where population elements are sampled.

    nsize: type=int
        Size of each sample.

    nsamples: type=int
        Number of samples to be drawn from 'lst'

    exclusives: type=list or type=dict
    '''
    samples = list(range(nsamples))#len=16
    inds = sample(range(0, len(lst)), nsize*nsamples)#len = 640
    exclusives = flatten(exclusives)
    for item in range(len(exclusives)):
        if item in flatten(inds) and item in exclusives:
            inds.remove(item)
    samples = [inds[ind:ind+nsize] for ind in range(0, len(inds), nsize)]
    try:
        for exclusive in exclusives:
            error_msg = 'non-exlusive samples'
            shared_items = []
            for item in flatten(samples):
                if item in flatten(exclusive):
                    shared_items.append(item)
        len(shared_items) != 0
        print(error_msg)
    except:
        return samples

def get_answers(rundict):
    '''
    Returns the answers based on keys pressed by subject
    in a list and adds this list as 'Answers' in 'self.rundict'.
    '''
    answerlist = []
    encnames = [rundict['encstims'][stim][0]
                for stim in range(len(rundict['encstims']))]
    encpos = [rundict['encstims'][stim][1]
              for stim in range(len(rundict['encstims']))]
    recnames = [rundict['recstims'][stim][0]
                for stim in range(len(rundict['recstims']))]
    recpos = [rundict['recstims'][stim][1]
              for stim in range(len(rundict['recstims']))]
    for ans in range(len(encnames)):
        if recnames[ans] in encnames:
            if recpos[ans] == encpos[ans]:
                answerlist.append('HIT')
            else:
                answerlist.append('WS')
        elif recnames[ans] not in encnames and recpos[ans] != 'None':
            answerlist.append('FA')
        else:
            answerlist.append('CR')
    rundict.update({'answers':answerlist})
    
def dict2csv(dict_item):
    ''' Description
    -----------
    Writes dict object to csv file\
    Returns
    -------
    None
    '''
    with open('test.csv', 'w') as file2write:
        for key in dict_item.keys():
            file2write.write("%s,%s\n"%(key, dict_item[key]))
#dict2csv(categories)

def renamefaces(facepath='/home/francois/cib/images/animate_being/animal/animal_face'):
    flist = list(dict.fromkeys([dname(item) for item in loadimages(facepath)]))
    for item in flist:
        if '_face' not in bname(item):
            os.rename(item, join(dname(item), bname(item)+'_face'))