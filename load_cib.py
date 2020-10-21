#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:50:46 2020

@author: francois
"""
import json
import os
from os.path import basename as bname
from os.path import join
from os import listdir as ls
from pandas import DataFrame as df
#THIS IA FOR TESTING
def main():
    '''
    'Overwrite current cib.json file in 'docs' directory.'''
    def loadimages(impath='../images'):
        '''Description
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

    def load_cib(imdir = '../images'):
        ''' Returns nested dictionairy with category infos'''
        baselvl = [join(imdir, item) for item in ls(imdir)] # animate_being, object, place
        mapping = df.from_dict(\
                    df((((bname(top), ('n_files', len(loadimages(top)))).__str__(),
                         ((dict((((sub1, ('n_files',\
                           len(loadimages(join(top, sub1))))).__str__(),\
                            dict((((sub2, ('n_files',\
                             len(loadimages(join(top, sub1, sub2))))).__str__(),\
                              dict((((sub3, ('n_files',\
                               len(loadimages(join(top, sub1, sub2, sub3))))).__str__(),\
                                dict(((((((item, ('n_files',\
                                 (len(loadimages(join(top, sub1,
                                                      sub2, sub3, item)))))).__str__(),\
                                  ('files', sorted(loadimages(join(
                                      top, sub1, sub2, sub3, item)))))))))
                                     for item in ls(join(top,sub1,sub2,sub3)))))
                                   for sub3 in ls(join(top,sub1,sub2)))))
                                 for sub2 in ls(join(top, sub1)))))\
                                for sub1 in ls(top)))))
                        for top in baselvl),
                       dtype='object').set_index(0).transpose(
                           ).to_dict()).transpose().to_dict()[1]
        return mapping
    def json_write(jsonfit, name='cib_inv.json'):
        with open(join('../docs/', name), 'w') as outfile:
            json.dump(json.dumps(jsonfit, indent=10), outfile)
    cibmap = load_cib()
    json_write(cibmap)
if __name__ == "__main__":
    main()
