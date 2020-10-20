#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 01:27:15 2020

@author: francois
"""
import os
from operator import itemgetter 
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from os.path import splitext
from random import sample
from typing import Sequence
import pandas as pd
from nltk.corpus import wordnet as wn
IMDIR = '../images'

# def big(datas):
#     datas['newsub'] = [[get_datas(sub) for sub in subs]
#                        for subs in datas.subs]
#     return datas
        
# def firstof(lst): 
#     return list( map(itemgetter(0), lst )) 

# def quickdf(imdir):
#     return pd.DataFrame(sorted(list(os.walk(imdir)))[1:],
#                           columns=['path', 'subordinates', 'concepts'])
# testdf = quickdf(imdir)
    # newd = pd.DataFrame((bname(fpaths.loc[ind]['path']), 
    #                      [os.path.abspath(item) for item in os.listdir(fpaths.loc[ind]['path'])])
    #                     for ind in fpaths.index)
                                            
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
    fpaths = pd.DataFrame(sorted(list(os.walk(imdir)))[1:],
                          columns=['path', 'subordinates', 'concepts'])
    # fpaths['names'] = [bname(row[1]['path']) for row in fpaths.iterrows()]
    
    # findex = pd.DataFrame(sorted(list(os.walk(imdir)))[1:],
    #                       columns=['path', 'subordinates', 'concepts'])

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
    # fpaths['tags_syns'] = [[syns.loc[tag]['syn']
    #                         for tag in fpaths.loc[ind].tags]
    #                        for ind in fpaths.index]
    # fpaths['subordinates_syns'] = [[syns['syn'][subordinate]
    #                                 for subordinate
    #                                 in fpaths.loc[ind].subordinates]
    #                                for ind in fpaths.index]
    return fpaths.set_index('names')
# toplevel = [join(IMDIR, item) for item in os.listdir(IMDIR)]
# levels = fpaths[['path', 'subs']]
# test2 = dict(((bname(dpath), get_datas(dpath)) for dpath in toplevel))
# test3 = pd.concat(test2.values(),  axis=1, keys=test2.keys())
# levels['subs2'] = [[[join(subpath, subitem) for subitem in os.listdir(subpath)]
#                    for subpath in sub]
#                    for sub in levels['subs']]

# bodies = get_datas(join(IMDIR, 'body'))
# faces
# findex = pd.DataFrame.from_dict(dict((row[0], row[1].subordinates) 
#                                      for row in folders.iterrows()), orient='index')

def get_folders(datas):
    ''' Description
        -----------
    '''
    folders = pd.DataFrame((row[1]for row in datas.iterrows()
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
    # if isinstance(datas, str) != True:
    #     datas=datas
    # else:
    #     datas = get_datas(datas)
    images = pd.DataFrame((row[1]for row in datas.iterrows()
                           if pd.isnull(row[1]['subordinates']).all()),
                          columns=list(datas.columns))
    # images['names'] = ['_'.join([bname(row[1]['path']),
    #                              bname(dname(row[1]['path']))])
    #                    for row in images.iterrows()]
    images['names'] = [' '.join([bname(dname(row[1]['path'])), bname(row[1]['path'])]) 
                       for row in images.iterrows()]
    images = images.set_index('names')
    return images.sort_index(kind='mergesort')

def bigdata(datas):
    datalst = []
    for fpath in datas.path:
        catlst = (bname(fpath), get_datas(fpath))
        datalst.append(catlst)
    return datalst
    # midx = pd.MultiIndex.from_tuples(datalst, names =('category', 'datas')) 
    # final = pd.DataFrame(((item[0], item[1]) for item in datalst.items()),
    #                      index=[item[0] for item in datalst.items()])
    return datalst
# big2 = bigdata(folders)
# test = bigdata(animals)

def get_data(imdir):
    data = get_datas(imdir)
    folders = get_folders(data)
    images = get_images(data)
    return data, folders, images 

    # for frow in folders.iterrows():
    #     if os.listdir(frow[1].subs[sub[0]])

# dirlist = get_data(imdir=IMDIR)


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
    # syns = pd.DataFrame(sorted(list(item for item in dict(zip(
    #             sorted(list(dict.fromkeys(\
    #                 sorted(list(dict.fromkeys(flatten(\
    #                 list(splitall(impath.split('../images')[1])[1:-1]
    #                      for impath in loadimages('../images'))))))).keys())),
    #             pd.read_excel(
    #                 '../docs/all_tags_and_synsets.xlsx').set_index(['syn'])['syn'])).items())),
    #                     columns=['tag', 'syn'])
    syns['syn'] = [wn.synset(syn).name() for syn in syns['syn']]
    return syns

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



#def csv2dict(file_path):
#    with open(file_path, mode='r') as infile:
#    reader = csv.reader(infile)
#    with open('coors_new.csv', mode='w') as outfile:
#        writer = csv.writer(outfile)
#        mydict = {rows[0]:rows[1] for rows in reader}
def q_rename(fpath, prefix=None):
    ''' Description
        -----------
        Quickly renames and indexes images in directory either by using\
            A) path components as tags joined together\
            B) user-defined perfix\
        Parameter(s)
        ------------
        fpath: path to image directory\
        prefix: deffaul=None\
                must be string\
        Variables
        ---------
        count: iterative integer to index each image\
        lst: list to save new image_concept names\
        Imported method(s)
        ------------------
        from os.path module: basename as bname, join, splitext\
        from os module: rename\
        Returns
        -------
        None
    '''
    count = 1
    lst = []
    for image in os.listdir(fpath):
        if prefix is None:
            prefix = '_'.join(reversed(list(\
                            splitall(fpath.split(IMDIR)[0])[-3:])))
        elif prefix is not None:
            prefix = str(prefix)
        if count <= 9:
            suffix = ''.join(['0'+str(count), splitext(image)[1]])
        else:
            suffix = ''.join([str(count), splitext(image)[1]])
        os.rename(join(fpath, image), join(fpath, prefix+suffix))
        count += 1
    return lst
# q_rename('/home/francois/Desktop/cnib_22july2020/images/animate_being/human/face/male/elder')


def renamefaces(facepath='/home/francois/cib/images/animate_being/animal/animal_face'):
    flist = list(dict.fromkeys([dname(item) for item in loadimages(facepath)]))
    
    for item in flist:
        if '_face' not in bname(item):
            os.rename(item, join(dname(item), bname(item)+'_face'))
renamefaces()
