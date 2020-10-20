#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 04:39:28 2020

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
from random import sample
import shutil
from tqdm import tqdm
from typing import Sequence
from taskfunctions import flatten
from taskfunctions import splitall

unique_syns = [concept[0] for concept in enumerate(unique) if en_lemmas.__contains__(concept)]
ANIMAL_PATH = '/home/francois/Desktop/neuromod_image_bank (copy)/animal/mammal/aquatic_mammal/beaver/face_beaver/face_beaver04.jpg'
syn_sets = [wn.synsets(token) for token in tokens]
split_syn_sets = [(syn_set.lemma_names(), syn_set.hyponyms()) for syn_set in syn_sets]

u_con = list(dict.fromkeys(c2))
syn = wn.synset('animate_being.n.01')
synonyms = []
antonyms = []
for l in syn.lemmas(): 
    synonyms.append(l.name()) 
    if l.antonyms(): 
        antonyms.append(l.antonyms()[0].name()) 