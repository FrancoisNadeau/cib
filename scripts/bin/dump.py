#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:14:24 2020

@author: francois
"""

#        datalist3 = list((((str(' '.join(reversed(splitall(\
#                             fpath.split('../images')[1])[1:][-2:]))),
#                            os.listdir(fpath)),
#                           OrderedDict((item, os.listdir(join(fpath, item)))
#                                       for item in folder),
#                           (len(imgs), imgs))
#                          for fpath, folder, imgs in os.walk('../images')))[1:]
#        datalist66 = sorted(list(((((splitall(fpath.split('../images')[1])[1:],
#                                   (len(os.listdir(fpath)), os.listdir(fpath)))),
#                                  tuple(os.listdir(join(fpath, item))
#                                   for item in folder),
#                                  (len(imgs), imgs)))
#                                 for fpath, folder, imgs
#                                 in os.walk('../images'))[1:])
#def find_matches(lst1, lst2, to_syn=False):
#    result = [[str(sub).replace(sub2[0], sub2[1]) for sub in list(lst1) for sub2 in lst2 if sub2[0] == sub]
#                 ]
#    if to_syn == True:
#        result = [[wn.synset(syn) for syn in name] for name in result]
#    return result  
#name_syn = [find_matches(list(name.split(' ', maxsplit=0)), syns, to_syn=True) for tags in fpaths.tags]

#def con2syn(word):
#    try:
#        ind = list(char.isnumeric() for char in str(word)).index(True)
#        return word.split(sep=word[ind], maxsplit=1)[0]
#    except: 
#        return word