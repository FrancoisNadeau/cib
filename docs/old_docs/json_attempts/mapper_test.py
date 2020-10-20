#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 07:51:47 2020

@author: francois
"""
from collections import Counter
from collections import namedtuple
import json
import numpy as np
from os.path import basename as bname
from os.path import join
from os import listdir as ls
import pandas as pd
from pandas import DataFrame as df
from taskfunctions import loadimages

testtuple = namedtuple('allimages', loadimages())
IMDIR = '../images'
levelA = [join(IMDIR, item) for item in ls(IMDIR)] # animate_being, object, place
mapper = df.from_dict(\
            df(((bname(top),
                           (df(((sub1,
                                 dict((sub2,
                                       (dict(
                                           (sub3,
                                            df(((imgs, pd.MultiIndex.from_tuples(((len(sorted(ls(join(top, sub1, sub2, sub3, imgs))))),
                                                          sorted(ls(join(top, sub1, sub2, sub3, imgs)))), names=['n_files', 'files']).to_frame())
                                                for imgs in ls(join(top,sub1,sub2,sub3))))
                                            # dict((item,
                                            #       (len(ls(join(top, sub1, sub2, sub3, item))),
                                            #        sorted(ls(join(top, sub1, sub2, sub3, item)))))
                                            #      for item in ls(join(top,sub1,sub2,sub3))
                                            #      )
                                            )
                                           for sub3 in ls(join(top,sub1,sub2)))))
                                      for sub2 in ls(join(top, sub1))))
                                for sub1 in ls(top))).set_index(0).to_dict()[1]))
                for top in levelA),\
   dtype='object').set_index(0).transpose().to_dict()).transpose().to_dict()[1]