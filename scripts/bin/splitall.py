#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 21:56:43 2020

@author: francois
"""

import numpy as np
import os
from os.path import basename as bname
from os.path import join
import pandas as pd
from tqdm import tqdm
from typing import Sequence

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def flatten(nestedlst):
    """
    Description
    -----------
    Returns unidimensional list from nested list using list comprehension.

    Parameters
    ----------
        nestedlst: list containing other lists etc.

    Variables
    ---------
        bottomElem: type = str
        sublist: type = list

    Return
    ------
        flatlst: unidimensional list
    """
    flatlst = [bottomElem for sublist in nestedlst
               for bottomElem in (flatten(sublist)
               if (isinstance(sublist, Sequence)
               and not isinstance(sublist, str))
               else [sublist])]
    return flatlst

def inventory(topdir='neuromod_image_bank'):
    dirlist = list(dict.fromkeys(flatten([bname(allpics[0]).split(sep='_')
                                         for allpics in os.walk(os.getcwd())
                                         if os.path.isdir(allpics[0])])))[3:]
    filelist = []
    for allpics in os.walk(os.getcwd()):
        for picture in allpics[2]:
            picpath = join(allpics[0], picture)
            if os.path.isfile(picpath):
                filelist.append(picpath)
    matrix = np.asarray(dirlist)
    matrix2 = np.asarray([flatten([part.split(sep='_')
                          for part in splitall(
                          fpath[fpath.find(topdir)+len(topdir)+1:])])
                          for fpath in filelist])
    matrix3 = np.empty(shape=(len(filelist), len(dirlist)), dtype=bool)
    for tags in enumerate(matrix2):
        for label in enumerate(matrix):
            matrix3[tags[0]][label[0]] = tags[1].__contains__(label[1])
    inventory_df = pd.DataFrame(matrix3,
                                index=[bname(fpath) for fpath in filelist],
                                columns=matrix)
    inventory_df.to_excel(join(os.getcwd(), topdir+'.xlsx'))
    
inventory('inv_df2')

def subdirs(path):
    """Yield directory names not starting with '.' under given path."""
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry.name
            
subdirs(os.getcwd())

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

tree = get_tree_size(IMDIR)