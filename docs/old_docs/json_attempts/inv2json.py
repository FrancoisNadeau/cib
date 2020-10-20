#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 02:25:44 2020

@author: francois
"""

from collections import Counter
import json
import numpy as np
from os.path import basename as bname
from os.path import join
from os import listdir as ls
import pandas as pd

IMDIR = '../images'
mappin['places']['scene']['outdoors']['urban_area']['city']['n_files']

levelA = [join(IMDIR, sub1) for sub1 in ls(IMDIR)] # animate_being, object, place
# mappin = pd.DataFrame.from_dict(\
#              pd.DataFrame(((bname(top),
#                             (pd.DataFrame(((sub1,dict((sub2,\
#                 (dict((sub3, (len(ls(join(top,sub1,sub2))),
#                               dict((item,\
#                     {'n_files': len(ls(join(top, sub1, sub2, sub3, item))),\
#                       'files': sorted(ls(join(top, sub1, sub2, sub3, item)))})
#                                   for item in ls(join(top,sub1,sub2,sub3)))))
#                     for sub3 in ls(join(top,sub1,sub2)))))\
#                     for sub2 in ls(join(top, sub1))))\
#                     for sub1 in ls(top))).set_index(0).to_dict()[1]))
#                           for top in levelA),\
#    dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]

# index_names = pd.DataFrame.from_dict(\
#             pd.DataFrame(((bname(top), (pd.DataFrame(((sub1, dict((sub2,\
#                 (dict((sub3, [item
#                                   for item in ls(join(top,sub1,sub2,sub3))])
#                     for sub3 in ls(join(top,sub1,sub2)))))\
#                     for sub2 in ls(join(top, sub1))))\
#                     for sub1 in ls(top))).set_index(0).to_dict()[1]))
#                           for top in levelA),\
#    dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]
mappin = df.from_dict(\
             df(((bname(top), (df(((sub1, dict((sub2,\
                (df(((sub3,
                       df.from_dict(dict((item,
                                          {'n_files':len(sorted(ls(join(top, sub1, sub2, sub3, item)))),
                                           'files': sorted(ls(join(top, sub1, sub2, sub3, item)))})
                                         for item in ls(join(top,sub1,sub2,sub3))), orient='index'))
                     for sub3 in ls(join(top,sub1,sub2))), columns=[['n_files', 'n_items']],
                    index=df(pd.Index(pd.DataFrame(ls(join(top, sub1, sub2, sub3))).index
                                   for sub3 in ls(join(top, sub1, sub2))))
                    )))
                                               for sub2 in ls(join(top, sub1))))
                                   for sub1 in ls(top))).set_index(0).to_dict()[1]))
                 for top in levelA),\
   dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]
datas_json = json.dumps(mappin, indent=12)
# .replace('{', '[').replace('}', ']').replace(':', ""))
datas_df = pd.read_json(datas_json, orient='index')
datas_df.to_csv('../docs/index_names.csv')
test = np.array([np.array(list(np.array(list(sub1)) for sub1 in val)) for val in datas_df.values])
with open('../docs/index_names.json', 'w') as outfile:
    json.dump(index_names, outfile, indent=8)
with open('../docs/index_names.json', 'r') as json_file:
    read_names = json.load(json_file)
# with open('../docs/index_names.json', 'w') as outfile:
#     json.load(index_names, outfile, indent=8)
df = pd.read_json(json.dumps(read_names))
df = pd.read_json('../docs/mapper.json', orient='string')
mapper_array = json.load('../docs/mapper.json')
pd.DataFrame(pd.MultiIndex.from)
def load_tester(path):
    with open(path) as f:
        data = json.load(f)
    print(data)
    return np.asarray(data)
mapper_array = load_tester('../docs/mapper.json')
[[[[key4 for key in level4level]]]]
wtf = pd.DataFrame(pd.read_json(json.dumps(level4)), index=[pd.read_json(json.dumps((item[1]))) for item in pd.read_json(json.dumps(level4)).items()])
wtf = pd.read_json(json.dumps(level4), orient='columns')
wtf2 = pd.read_json(json.dumps(level4), orient='index')
wtf3 = wtf2.set_index(row[1].transpose() for row in wtf2.iterrows())
testarray = np.array(list(lvl1 for lvl1 in level4.items()))
wtf = pd.DataFrame.from_records(level4, index=[{(outerKey, innerKey): values for outerKey, innerDict in pd.DataFrame.from_dict(level4, orient='columns').iteritems() for innerKey, values in innerDict.items()}])
mappin_json2 = json.dumps(mappin_json)
testdf = pd.read_json(mappin_json)
testarray = np.array(level4).tolist()
test = json.dumps(testarray, indent=4)
parsed = json.dumps(test,)
emptydf = pd.MultiIndex.from_frame(pd.DataFrame.from_records(parsed))
test3 = np.array(test)
testdf = pd.read_json(json.loads(parsed), orient='records')
testdf2 = pd.DataFrame.from_records(test)
testjson = json.loads(json.dumps(test))
testdf.to_json('../docs/testdf2.json', orient='index')
readtest = pd.read_json("../docs/testdf2.json", orient='columns').to_dict()
all(readtest.notnull() == testdf.notnull())
test2 = readtest.to_json(orient='index', indent=4)
testdf2 = pd.read_json(test2, orient='index')
testdf2.to_json('../docs/testdf2.json', orient='index')
all(testdf2.notnull() == testdf.notnull())

def get_word_freqs(datas):
    ''' Description
        -----------
        Returns a Counter object counting how often each synset appears\
        in the database, either as image, category, tag, subordinate.
    '''
    return pd.Series(dict(Counter(datas))).sort_index()