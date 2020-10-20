#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 23:35:21 2020

@author: francois
"""

def inventorize(topdir=IMDIR):
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
    return inventory_df
#image10k = inventory()