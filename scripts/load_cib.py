#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:50:46 2020

@author: francois
"""
import json
from os.path import basename as bname
from os.path import join
from os import listdir as ls
from pandas import DataFrame as df
from taskfunctions import loadimages

def main():
    '''
    'Overwrite current cib.json file in 'docs' directory.
    '''
    def load_cib(imdir = '../images'):
        baselvl = [join(imdir, item) for item in ls(imdir)] # animate_being, object, place
        mapping = df.from_dict(\
                    df((((bname(top), ('n_files', len(loadimages(top)))),
                         ((dict((((sub1, ('n_files',\
                           len(loadimages(join(top, sub1))))),\
                            dict((((sub2, ('n_files',\
                             len(loadimages(join(top, sub1, sub2))))),\
                              dict((((sub3, ('n_files',\
                               len(loadimages(join(top, sub1, sub2, sub3))))),\
                                dict(((((((item, ('n_files',\
                                 (len(loadimages(join(top, sub1,
                                                      sub2, sub3, item)))))),\
                                  ('files', sorted(loadimages(join(
                                      top, sub1, sub2, sub3, item)))))))))
                                     for item in ls(join(top,sub1,sub2,sub3)))))
                                   for sub3 in ls(join(top,sub1,sub2)))))
                                 for sub2 in ls(join(top, sub1)))))\
                                for sub1 in ls(top)))))
                        for top in baselvl),
                       dtype='object').set_index(0).transpose(
                           ).to_dict()).transpose().to_dict()[1]
        return str(mapping)
    def json_write(jsonfit, name='cib_inv.json'):
        with open(join('../docs/', name), 'w') as outfile:
            json.dump(json.dumps(jsonfit), outfile, indent=8)
    cibmap = load_cib()
    json_write(cibmap)
if __name__ == "__main__":
    main()
