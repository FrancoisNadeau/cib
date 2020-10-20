#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:11:56 2020

@author: francois
"""
import json
from os.path import basename as bname
from os.path import join
from os import listdir as ls
import pandas as pd
from pandas import DataFrame as df
IMDIR = '../images'

# def inv_map(imdir=IMDIR):
#     levelA = [join(IMDIR, item) for item in ls(IMDIR)] # animate_being, object, place
#     mappin = df.from_dict(\
#                   df(((bname(top),
#                       (df(((sub1,
#                             dict((sub2,
#                                   df.from_records(((pd.Index(row[1], name=row[0]).to_frame()
#                                                     for row in df.from_dict(dict((item,
#                                                                                   {'n_files':len(sorted(ls(join(top, sub1, sub2, sub3, item)))),
#                                                                                     'files': sorted(ls(join(top, sub1, sub2, sub3, item)))})
#                                                                                   for item in ls(join(top,sub1,sub2,sub3))), orient='index'
#                                                                             ).iterrows()
#                                                     )
#                                                     for sub3 in ls(join(top,sub1,sub2)))))
#                                   for sub2 in ls(join(top, sub1))))
#                             for sub1 in ls(top))).set_index(0).to_dict()[1]))
#                       for top in levelA),
#                     dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]
#     return mappin

def inv_map(imdir=IMDIR):
    levelA = [join(IMDIR, item) for item in ls(IMDIR)] # animate_being, object, place
    mappin = df.from_records(df.from_dict(\
                  df.from_records((((bname(top),
                      (df.from_records((((sub1,
                            dict((sub2,
                                      df.from_records(
                                          (
                                              (
                                                  pd.Index(pd.Series(col),
                                                           name=col[0]).to_frame().set_index([[0, 1]])
                                                  for col in pd.Index(df.from_dict(dict((item,
                                                                                         {'n_files':len(sorted(ls(join(top, sub1, sub2, sub3, item)))),
                                                                                          'files': sorted(ls(join(top, sub1, sub2, sub3, item)))})
                                                                                        for item in ls(join(top,sub1,sub2,sub3))), orient='index'
                                                                                   )
                                                                      ).to_frame().iteritems()
                                                  )
                                              for sub3 in ls(join(top,sub1,sub2))
                                              )
                                          ).set_index(pd.Index(ls(join(top,sub1,sub2))))
                                  )
                                 for sub2 in ls(join(top, sub1))))
                           for sub1 in ls(top)))).set_index(0).to_dict()[1]))
                      for top in levelA))).set_index(0).transpose().to_dict()).transpose().to_dict()[1]).to_dict()
    return mappin

mappin = inv_map(IMDIR)

mml = mappin['animate_being']['animal']['mammal']

# def inv_map(imdir=IMDIR):
#     levelA = [join(IMDIR, item) for item in ls(IMDIR)] # animate_being, object, place
#     mappin = df.from_dict(\
#                  df(((bname(top),
#                       (df(((sub1,
#                             dict((sub2,
#                                   df.from_records(((pd.Index(row[1], name=row[0]).to_frame()
#                                                     for row in df((len(sorted(ls(join(top, sub1, sub2, sub3, item)))),
#                                                                    sorted(ls(join(top, sub1, sub2, sub3, item))))
#                                                                                   {'':,
#                                                                                    'files': })
#                                                                                  for item in ls(join(top,sub1,sub2,sub3))
#                                                                             ).iterrows()
#                                                     )
#                                                    for sub3 in ls(join(top,sub1,sub2)))))
#                                  for sub2 in ls(join(top, sub1))))
#                            for sub1 in ls(top))).set_index(0).to_dict()[1]))
#                      for top in levelA),
#                     dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]
#     return mappin

reform = {(outerKey, innerKey): values 
              for outerKey, innerDict in mappin.items()
              for innerKey, values in innerDict.items()}
test = json.dumps(mappin.to_json(orient='index'), indent=16)
testread = pd.read_json(test, orient='str',)
testdf = pd.read_json(test, orient='index').transpose()
testdf.to_json('../docs/testdf2.json', orient='index')
testload = json.loads('../docs/testdf2.json')
readtest = pd.read_json("../docs/testdf2.json", orient='index')
all(readtest.notnull() == testdf.notnull())
test2 = readtest.to_json(orient='index', indent=4)
testdf2 = pd.read_json(test2, orient='index')
testdf2.to_json('../docs/testdf2.json', orient='index')
all(testdf2.notnull() == testdf.notnull())
mappin2 = dict((key,value) for key, value in testdf2.skipna().to_dict(orient='index').items())
testdf3 = pd.read_json(pd.json_normalize(mappin), orient='index')
df = pd.concat({k: df(v) for k, v in mappin.items()}).unstack(0).swaplevel(1,0, axis=1).sort_index(axis=1)
with open('../docs/testdf2.json') as data_file:    
    df2 = json.load(data_file)