#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 04:37:13 2020

@author: francois
"""

from functools import reduce
import json
from nltk.corpus import wordnet as wn
import numpy as np
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
import pandas as pd
from PIL import Image
from random import sample
import shutil
from tqdm import tqdm
from typing import Sequence
from taskfunctions import flatten
from taskfunctions import splitall

#picpath = '/home/francois/Desktop/banque_finale_apr12_b/images/animate_being/animal/body/bird/blue_jay/body_blue_jay/body_blue_jay01.jpg'

IMDIR = '/home/francois/Desktop/banque_finale_apr12_d/images'
total = len(loadimages(IMDIR))

def get_extra_images():
    EXTRADIR = '/home/francois/Desktop/banque_finale_apr12_c/extra_images'
    extradirs = []
    piclist = list(dict.fromkeys((bname(dname(join(allpics[0], pic))),
                    os.listdir(dname(join(allpics[0], pic))))
                    for allpics in os.walk(EXTRADIR):
                    for pic in allpics[2]
    unique_pics = dict(list(dict.fromkeys(piclist)))
    piclist_test = dict.fromkeys(piclist)
    piclist_test2 = dict(piclist)
        for picdir in allpics[1]:
            dirpath = join(allpics[0], picdir)
            extradirs.append((bname(dirpath), os.listdir(dirpath)))
    extradict = dict(extradirs)
    extradf = pd.DataFrame.from_dict(extradict, orient='index')
    return extradf

extra_images = get_extra_images()

def do_it(imdir=IMDIR):
    objlist = []
    for allim in os.walk(IMDIR):
        for pic in allim[2]:
            picpath = join(allim[0], pic)
            if 'panda' in picpath:
                newdir = join(dname(dname(picpath)), 'giant_panda')
                if os.path.exists(newdir) != True:
                    os.mkdir(newdir)
                    shutil.move(picpath, join(newdir, pic))
do_it()
#            picdir = (len(os.listdir(dname(join(allim[0], pic)))),
#                      dname(join(allim[0], pic)))
#            if picdir[0] < 20:
#                to_increase.append((picdir[0], picdir[1]))
#            if picdir[0] > 20:
#                to_decrease.append((picdir[0], picdir[1]))
#            if picdir[0] <= 10:
#                low_counts.append((picdir[0], picdir[1]))
objlist = do_it(IMDIR)
###############################################################################
#def get_humans():
#    human_dirs = []
#    for allpics in os.walk(IMDIR):
##    for pic in allpics[2]:
##        picpath = join(allpics[0], pic)
##        if 'human' in picpath and 'animal' not in picpath:
##            human_dirs.append((bname(dname(picpath)),
##                               len(os.listdir(dname(picpath)))))
#        for picdir in allpics[1]:
#            dirpath = join(allpics[0], picdir)
#            if 'human' in dirpath and 'animal' not in dirpath:
#                human_dirs.append((bname(dirpath),
#                                   len(os.listdir(dirpath))))
#    human_dirlist = list(dict.fromkeys(human_dirs))            
#    humandf = pd.DataFrame(human_dirlist)
#    return humandf

def get_humans():
    human_dirs = []
    human_picdirs =[]
    for allpics in os.walk(IMDIR):
        for pic in allpics[2]:
            picpath = join(allpics[0], pic)
            if 'human' in picpath and 'animal' not in picpath:
                human_picdirs.append((bname(dname(picpath)),
                                   len(os.listdir(dname(picpath)))))
        for picdir in allpics[1]:
            dirpath = join(allpics[0], picdir)
            if 'human' in dirpath and 'animal' not in dirpath:
                human_dirs.append((bname(dirpath),
                                   len(os.listdir(dirpath))))
    human_piclist = list(dict.fromkeys(human_picdirs))
    human_dirlist = list(dict.fromkeys(human_dirs))
    human_tags = [tag for tag in human_dirlist if tag not in human_piclist]         
    humandf = pd.DataFrame(human_tags)
    return humandf

humans = get_humans()

#extras for implementing WN to Image10k
#    ani_sheet = pd.read_excel(join(dname(IMDIR),'docs', 
#                                   'animal_synsets.xlsx'))\
#                                   ['animal_synsets'].to_list()
#    ani_syns = [syn.name() for syn in en_allsyns if ani_sheet.__contains__(syn.name())]
#    newsyns = [(name.split(sep='.')[0], wn.synset(name)._lemma_names[0]) 
#               for name in ani_sheet if not ani_syns.__contains__(name)]
#    to_rename = []
#    '''Specific function for uniformizing file, folder and  extension names.'''
#    olds = [newsyn[0] for newsyn in newsyns]
#    news = [newsyn[1] for newsyn in newsyns]
#filepath1 = '/home/francois/Desktop/banque_finale_apr10_a/images/animate_being/animal/face/bird/falcon/face_falcon/face_falcon/face_falcon03.jpg'