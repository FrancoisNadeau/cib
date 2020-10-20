#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:55:29 2020

@author: francois
"""
from collections import Counter
import json
import numpy as np
from os.path import basename as bname

from os.path import dirname as dname
from os.path import join
from os import listdir as ls
import pandas as pd
from pandas import DataFrame as df
from taskfunctions import flatten
from taskfunctions import loadimages
from taskfunctions import splitall

with open('../docs/index_names.json', 'r') as json_file:
    read_names = json.load(json_file)
datas_json = json.dumps(cib_json)

allim = loadimages()
tags = flatten([splitall(dname(fpath).split(IMDIR)[1])[1:] for fpath in allim])
freqs = [dict((tag, Counter(bname(dname(tag))).values()) for tag in flatten(tags))]
freqs = pd.Series(dict(Counter(flatten(tags)))).sort_index()
json_mapper = json.dumps(cib_json)
json_mapper
json_freqs = freqs.to_json()
freq_json = json.dumps(freqs, indent=4)

def flatten_json(dictionary):
    flattened = []

    def flat(data, name=''):
        if type(data) is dict:
            for d in data:
                flat(data[d], name + d + ',')
        elif type(data) is list:
            i = 0
            for l in data:
                flat(l, name[:-1] + '_' + str(i) + ',')
                i += 1
        else:
            flattened.append((name[:-1] + ',' + data).split(','))

    flat(dictionary)
    return flattened

list_obj=flatten_json(cib_json)
final = df(list_obj).set_index(list(range(len(list_obj[0])-1)))

final.to_json('../docs/final_test.json')
dat0 = json.load('../docs/final_test.json', orient='index')
dat = pd.Index(pd.read_json('../docs/final_test.json', orient='index')).to_frame(index=[0])
dat = pd.Index(dat.reindex(dat.index))
final.head()
###############################################################################

with open(json_mapper, 'r') as file:
     json_data = json.load(file)
     for jdata in json_data:
         for freq in freqs:
             if freq[0] in jdata:
                 jdata = jdata.replace(freq[0], freq)
with open('../docs/newvalues.json', 'w') as file:
    json.dump(json_data, file, indent=16)

dictionary = flatten_json(test)
all_values = list(dictionary.values())

index_list = []
for key in dictionary:
    x = tuple(key.split("-"))
    index_list.append(x)

index = pd.MultiIndex.from_tuples(index_list)

bigdata = pd.Series(all_values, index=index).to_frame()