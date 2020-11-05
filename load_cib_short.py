#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:23:41 2020

@author: francois
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:50:46 2020

@author: francois
"""
import os
from os.path import basename as bname
from os.path import join
from os import listdir as ls
import pandas as pd
from pandas import DataFrame as df
from cib_utils import json_write

def main():
    ''' Overwrite current cib.json file in 'docs' directory.
        N.B: Move/rename existing 'cib_inv.json' file to prevent overwriting
    '''
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
        # animate_being, object, place
        baselvl = [join(imdir, item) for item in ls(imdir)]
  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:50:46 2020

@author: francois
"""
import os
from os.path import basename as bname
from os.path import join
from os import listdir as ls
from pandas import DataFrame as df
from cib_utils import json_write

def main():
    ''' Overwrite current cib.json file in 'docs' directory.
        N.B: Move/rename existing 'cib_inv.json' file to prevent overwriting
    '''
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

    def load_cib_short(imdir = '../images'):
        ''' Returns nested dictionairy with category infos'''
        # animate_being, object, place
        baselvl = [join(imdir, item) for item in ls(imdir)]
        mapping = df.from_dict(\
                    df((((bname(top), len(loadimages(top))).__str__(),
                         (dict(
                             ((sub1, len(loadimages(join(top, sub1)))).__str__(),\
                            dict(
                                ((sub2, len(loadimages(join(top, sub1, sub2)))).__str__(),
                              dict(
                                  ((sub3,
                                    len(loadimages(join(top, sub1,
                                                        sub2, sub3)))).__str__(),\
                                dict(
                                    (item, len(loadimages(join(top, sub1, sub2, sub3, item))))
                                     for item in ls(join(top, sub1, sub2, sub3))))
                                   for sub3 in ls(join(top,sub1,sub2))
                                   ))
                                 for sub2 in ls(join(top, sub1))
                                 ))\
                                for sub1 in ls(top))
                                 ))
                        for top in baselvl),
                       dtype='object').set_index(0).transpose(
                           ).to_dict()).transpose().to_dict()[1]
        return mapping
    cibmap = load_cib_short()
    json_write(cibmap, name='cib_map_short')
if __name__ == "__main__":
    main()
# tree = json_read('/home/francois/cib/cib_docs/cib_map_short666.json')
# tress_str = json.dumps(tree, indent=36)