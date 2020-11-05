#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:24:53 2020

@author: francois
"""
from collections import Counter
import json
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from typing import Sequence
import pandas as pd
from pandas import DataFrame as df
from nltk.corpus import wordnet as wn

IMDIR = '../images'

def count_categs():
    imtags =  pd.read_csv('image_tags.csv')
    return Counter(list(imtags[['level0', 'level1', 'level2', 'level3', 'level4']].values.flat))
catcount = count_categs()
def json_read(fpath):
    ''' Read JSON file to Python object.
        Parameter(s)
        -------------
        fpath:   str/path-like object (default='.' <cib_docs>)
        
        Reminder from native json module docs:
            JSON to Python conversion list
                JSON	PYTHON
                object*	dict    includes pandas DataFrame objects
                array	list
                string	str
                number (int)	int
                number (real)	float
                true	True
                false	False
                null	None
        Return
        ------
        Python object
    '''
    with open(fpath, "r") as read_file:
        return json.loads(json.load(read_file))
    
def json_write(jsonfit, fpath='.', name='cib_inv', idt=None):
    ''' Write JSON compatible python object to desired location on disk
        
        Parameters
        ----------
            jsonfit: JSON compatible object
                     Object to be written on disk.
                     See list below (from native JSON documentation)
            fpath:   str/path-like object (default='.' <cib_docs>)
                     Path where to save. All directories must exist
            name:    String (default='cib_inv')
                     Desired filename to save
            idt:     Non-negative Int (default=None)
                     Indentation for visibility
                     *From native JSON docs: 
                         If ``indent`` is a non-negative integer,
                         then JSON array elements and object members
                         are pretty-printed with that indent level.
                         Indent level 0 only inserts newlines. 
                         ``None`` is the most compact representation.
                              
            JSON to Python conversion list
                JSON	PYTHON
                object*	dict    includes pandas DataFrame objects
                array	list
                string	str
                number (int)	int
                number (real)	float
                true	True
                false	False
                null	None
            
        Return
        ------
        None
    '''
    with open(join(fpath, name+'.json'), 'w') as outfile:
        json.dump(json.dumps(jsonfit, indent=idt), outfile)

                                            
def splitall(path):
    ''' Description
        -----------
        Returns tuple containing each directory in path to file
    '''
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
    return tuple(allparts)

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
               for bottomElem in (flatten(sublist)\
               if (isinstance(sublist, Sequence)\
               and not isinstance(sublist, str)) else [sublist])]
    return flatlst

def get_datas(imdir=IMDIR):
    '''Description
       -----------
       Uses os.walk to recursively ascend CNIB/images directory.\
       Allows to keep structure\
       Also incorporates WordNet with 'get_synsets' method.\
       Returns
       -------
       CNIB.datas: DF containing both images and categories.\
       Columns = 'path': path to item in database
                 'subordinates': folders contained inside an item in datas\
                                 provided the item is a directory\
                 'concepts': images contained in a lower-level category\
                 'tags': each superordinate category a concept belongs to\
                 n_items': number of times a concept is represented\
                 'tags_syns': 'tags' converted to proper synset\
                 'subordinates_syns': 'subordinates' converted to \
                                       proper synset\
                 'freq_tags': Counter object for total occurence of \
                              each concept in CNIB
    '''
    # syns = get_synsets()
    fpaths = df(sorted(list(os.walk(imdir)))[1:],
                          columns=['path', 'subordinates', 'concepts'])
    fpaths['subs'] = [[join(fpath, item) for item in os.listdir(fpath)]
                      for fpath in fpaths.path]
    fpaths['tags'] = [splitall(fpath.split(imdir)[1])[1:]
                      for fpath in fpaths['path']]
    # fpaths['concepts'] = fpaths['concepts'].sort_index()
    fpaths['n_items'] = [len(os.listdir(path))
                         for path in fpaths['path']]
    fpaths['freq_tags'] = [[row[1].tags*row[1].n_items]
                           for row in fpaths.iterrows()]
    fpaths['names'] = [bname(fpath) for fpath in fpaths.path]
    folders = get_folders(fpaths)
    images = get_images(fpaths)
    # fpaths['tags_syns'] = [[syns.loc[tag]['syn']
    #                         for tag in fpaths.loc[ind].tags]
    #                        for ind in fpaths.index]
    # fpaths['subordinates_syns'] = [[syns['syn'][subordinate]
    #                                 for subordinate
    #                                 in fpaths.loc[ind].subordinates]
    #                                for ind in fpaths.index]
    return fpaths, folders, images

def get_folders(datas):
    ''' Description
        -----------
    '''
    folders = df((row[1]for row in datas.iterrows()
                           if not all(pd.isnull(row[1]['subordinates']))),
                          columns=list(datas.columns))
    folders['names'] = [bname(folders.loc[ind]['path'])
                       for ind in folders.index]
    folders = folders.set_index('names')
    return folders.sort_index(kind='mergesort')

def get_images(datas):
    ''' Description
        -----------
        DF containing each image_concept\
        Returns
        -------
        ImageBank.images
    '''
    images = df((row[1]for row in datas.iterrows()
                           if pd.isnull(row[1]['subordinates']).all()),
                          columns=list(datas.columns))
    images['names'] = [bname(row[1]['path'])
                       for row in images.iterrows()]
    images['folders'] = [bname(dname(row[1].path)) for row in images.iterrows()]
    images = images.set_index('folders')
    # images_ind = images.set_index('names', append=True).index
    return images.sort_index(kind='mergesort')


def get_data(imdir):
    ''' Shortcut function to load info about all images and categories. '''
    data = get_datas(imdir)
    folders = get_folders(data)
    images = get_images(data)
    return data, folders, images 
    
def loadimages(impath='../images'):
    '''
    Description
    -----------
    Lists the full relative path of all '.jpeg' files in a directory.

    Parameters
    ----------
    imdir: type = str
        Name of the directory containing the images.

    Return
    ------
    imlist: type = list
        1D list containing all '.jpeg' files' full relative paths
    '''
    imlist = []
    for allimages in os.walk(impath):
        for image in allimages[2]:
            impath = join(allimages[0], image)
            if os.path.isfile(impath):
                imlist.append(impath)
    return imlist

def get_synsets():
    ''' Description
        -----------
        DF containg each tag associated to proper WN synset\
            columns = 'syn': synset object manually chosen\
                      *As listed in cnib/docs/all_synsets.xlsx*\
        Returns
        -------
        syns
    '''
    syns = pd.read_excel('../docs/all_tags_and_synsets.xlsx').set_index(['tags'])
    # syns = df(sorted(list(item for item in dict(zip(
    #             sorted(list(dict.fromkeys(\
    #                 sorted(list(dict.fromkeys(flatten(\
    #                 list(splitall(impath.split('../images')[1])[1:-1]
    #                      for impath in loadimages('../images'))))))).keys())),
    #             pd.read_excel(
    #                 '../docs/all_tags_and_synsets.xlsx').set_index(['syn'])['syn'])).items())),
    #                     columns=['tag', 'syn'])
    syns['syn'] = [wn.synset(syn).name() for syn in syns['syn']]
    return syns

def clean_imname(name):
    ''' Description
        -----------
        Returns unique image_concept string* in directory
        *stripped from manual indexing and file exetension\
        *Resolves the issue of each 'body_part' image_concept having\
         'body_part_' in them since it is already counted as a tag.\
        Returns
        -------
        name: string
    '''
    if not name.isalpha():
        n_ind = [char.isnumeric() for char in iter(name)]
        name = name.split(name[n_ind.index(True)])[0]
        if 'body_part' in name:
            name = name.replace('body_part_', '')
        return name
