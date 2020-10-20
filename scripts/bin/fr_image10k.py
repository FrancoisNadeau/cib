#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:58:07 2020

@author: francois
"""

import copy
from nltk.corpus import wordnet as wn
import numpy as np
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
import pandas as pd
#from taskfunctions import flatten
#from taskfunctions import splitall
#from taskfunctions import inventory
from translate import Translator
from tqdm import tqdm
from typing import Sequence
#from googletrans import Translator
import xml.etree.ElementTree as ET
import xml.dom.minidom
import xmltodict
import json

def flatten(nestedlst):
    flatlst = [bottomElem for sublist in nestedlst
               for bottomElem in (flatten(sublist)
               if (isinstance(sublist, Sequence)
               and not isinstance(sublist, str))
               else [sublist])]
    return flatlst
XMLDOC = '/home/francois/Desktop/wonef-precision-0.1.xml'
XMLDOCBIG = '/home/francois/Desktop/wolf-1.0b4.xml'
translator = Translator(to_lang='fr')
IMDIR = '/home/francois/Desktop/neuromod_image_bank/images'
INVPATH = '/home/francois/Desktop/neuromod_image_bank/images/inventory_df.xlsx'
DEFS = '/home/francois/Documents/image10k_definitions_en.xlsx' 

def xml_to_dict(docpath=XMLDOC):
    xmltree = ET.parse(docpath)
    xml_data = xmltree.getroot()
#    children = xml_data.getchildren() #can be useful for labeling
    # Here you can change the encoding type
    xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
    data_dict = dict(xmltodict.parse(xmlstr))
    return data_dict
#DATADICT = xml_to_dict()
#en_allsyns = list(wn.all_synsets())

def get_fr_n_dict():
    fr_allsyns = xml_to_dict(XMLDOC)['WN']['SYNSET']
    keys = []
    values = []
    for syn in fr_allsyns:
        if syn['POS'] == 'n':
            frw = dict(syn)
            fr_syn = {}
            key = syn['ID'][7:-2]
            newkey = key.lstrip('0')
            keys.append(newkey)
            synkeys = frw.keys()
            if 'ILR' in synkeys:
                fr_syn['ILR'] = frw['ILR'] 
            fr_syn['synonym'] = [(key, val) for key, val in syn['SYNONYM'].items()]
            fr_syn['definition'] = syn['DEF']
            values.append(fr_syn)
    fr_n_dict = dict(zip(keys, values))
    return fr_n_dict
fr_n_dict2 = get_fr_n_dict()

#def get_fr_defs():
#    translator = Translator(to_lang='fr')
#    fr_defs = []
#    defs = pd.read_excel(DEFS)['english definition from WN'].tolist()
#    for defin in enumerate(defs):
#        fr_defs.append(translator.translate(str(defin[1]), dest='fr').text)
#    return fr_defs
#fr_defs = get_fr_defs()

IMDIR = '/home/francois/Desktop/cnib_prefinal/images'
def get_im10k():
    unique3 =  list(dict.fromkeys([bname(join(allimages[0], category))
                                  for allimages in os.walk(IMDIR)
                                  for category in allimages[1]]))
    
    en_allsyns = list(wn.all_synsets())
    fr_n_dict = get_fr_n_dict()
    en_names = [syn for syn in en_allsyns if syn.pos() == 'n']
    database = dict(zip([s._name for s in en_allsyns
                         if s._lemma_names[0] in unique],
                        [(fr_n_dict[str(s._offset)],
                          s._lemma_names,
                          translator.translate(s._lemma_names[0]),
                          s._offset,
                          s._definition,
                          translator.translate(s._definition))
#                          fr_n_dict[str(s._offset)][1]
#                          fr_n_dict[str(s._offset)]['SYNONYM']
                         for s in en_names
                         if s._lemma_names[0] in unique]))
#                         [fr_n_dict[str(syn)][1] for syn in fr_n_dict]))
#    database_df = pd.DataFrame(database)
#    database_df.to_excel(join(dname(IMDIR),'database_df.xlsx'))
    return database


    
image10k = get_im10k()    
image10k_df = pd.DataFrame(image10k)
image10k_df.to_excel(join(os.getcwd(), 'Documents', 'image10k_df.xlsx'))

fr_definitions = []  
for synset in image10k.values:
    fr_def = translator.translate(str(synset)[0], dest='fr')
    fr_definitions.append(fr_def)
    
    CONCEPTS = '/home/francois/GitHub/ImageTask/concepts2.xlsx'
unique =  list(dict.fromkeys([bname(join(allimages[0], category))
                              for allimages in os.walk(IMDIR)
                              for category in allimages[1]]))
pd.DataFrame(unique, columns=['concepts']).to_excel(join(os.getcwd(),
                                                         'concepts.xlsx'))
pd.DataFrame(concepts, columns=['concepts']).to_excel(join(os.getcwd(),
                                                         'concepts2.xlsx'))
pd.DataFrame(diff, columns=['concepts']).to_excel(join(os.getcwd(),
                                                         'concepts3.xlsx'))
en_allsyns = list(wn.all_synsets())
concepts = list(dict.fromkeys(pd.read_excel(CONCEPTS)['names'].tolist()))
diff = [uni[0] for uni in enumerate(unique) if concepts.__contains__(uni)]
diff = [item for item in unique if item not in concepts]

concepts = [concept.split('.')[0] for concept in concepts]
ucons = [uni for uni in unique if concepts.__contains__(uni)]
diff = [uni for uni in unique if ]
c2 = []
for concept in unique:
    if en_lemmas.__contains__(concept):
        c2.append(concept)
        
en_names = [syn._name for syn in en_allsyns if syn.pos() == 'n']
en_lemmas = [syn._lemma_names[0] for syn in en_allsyns if syn.pos() == 'n']
#root = ET.fromstring(xmlstr)
#children2 = [(child.tag, child.attrib) for child in root]
#child_dict = dict.fromkeys(children)
#g_children = [(child.tag, child.attrib) for child in children]
#wn_dict = xmltodict.parse(XMLDOCBIG, xml_attribs=True)
# now I remove duplicities - by convertion to set and back to list
#elemList = lisitemt(set(elemList))
#fr_verbs = []
#fr_nouns = [s for s in fr_allsyns if s['POS'] == 'n']
#for noun in fr_nouns:
#    noun['ID'] = str(noun['ID'][7:-2]).lstrip('0')
#    print(noun['ID'])
#fr_adjectives = []
#for synset in synsets:
#    if synset.get('POS') == 'n':
#        fr_nouns.append(synset)
#    if synset.get('POS') == 'v':
#        fr_verbs.append(synset)
#    if synset.get('POS') == 'a':
#        fr_adjectives.append(synset)
#keys = [s._lemma_names[0] for s in en_allsyns]
#en_nouns = [s for s in en_allsyns if s.pos() == 'n']
#for noun in en_nouns:
#    if str(noun._offset).startswith('1'):
#        print(noun._offset)
#en_verbs = [s for s in allsyns if s.pos() == 'v']
#en_n_lemmas = [(n._lemma_names[0], n._name) for n in en_nouns]
#en_adjectives = [s for s in allsyns if s.pos() == 'a']
#offsets_list = [(s.offset(), s) for s in allsyns]
#offsets_dict = dict(offsets_list)
#offsets_dict[02623136]

# Just printing out the result
print(elemList)
doc = xml.dom.minidom.parse('/home/francois/Desktop/wolf-1.0b4.xml')
e = ET.fromstring(response.content)
translatedList = []
for index, row in pd.DataFrame(unique).iterrows():
    # REINITIALIZE THE API
    translator = Translator()
    newrow = copy.deepcopy(row)
    try:
        # translate the 'text' column
        translated = translator.translate(row['text'], dest='en')
        newrow['translated'] = translated.text
    except Exception as e:
        print(str(e))
        continue
    translatedList.append(newrow)
    



u_df = pd.DataFrame(unique)
fr_tags = []
for word in unique:
    trans = Translator()
    trs = translator.translate(word, dest='fr', src='en')
    mot = print(trs.text)
    fr_tags.append(mot)
    
translations = {}
for column in u_df.columns:    # Unique elements of the column    unique_elements = df[column].unique()
    for element in u_df[column]:        # Adding all the translations to a dictionary (translations)        
        translations[element] = translator.translate(element).text
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.fr',
    ])
u_np = np.array(unique)

tagstrings = []
for allpics in os.walk(IMDIR):
    for picture in allpics[2]:
        if picture.endswith('.jpg'):
            tagstr = splitall(str(join(allpics[0], picture)).split(IMDIR)[1])[1:-1]
            tagstrings.append(tagstr)
nptags = np.array(tagstrings)
bigstr = str(flatten(tagstrings))
animate_tags = []
for taglist in tagstrings:
    if taglist.__contains__('animate'):
        animate_tags.append(taglist)
bigatag = str(flatten(animate_tags))
animate_labels = []
for concept in unique:
    value = bigatag.count(concept)
    if value != 0:
        animate_labels.append((concept, value))
animate_labels_df = pd.DataFrame(animate_labels)
animate_labels_df.to_excel(join(IMDIR, 'animate_labels_df.xlsx'))
labels = []
for concept in unique:
    value = bigstr.count(concept)
    labels.append((concept, value))
labelsdf = pd.DataFrame(labels)
labelsdf.to_excel(join(IMDIR, 'labelsdf.xlsx'))
    
tagstrings = flatten(tagstrings)
tstr = str(tagstrings)
tstr.count(unique[0])
imlabels = []
for allim in os.walk(IMDIR):
    for picture in allim[2]:
        if picture.endswith('.jpg'):
            for c in picture:
                if c.isdigit():
                    picture = picture[:picture.index(c)]
            imlabels.append(pic)
            
name = 'francois01'
sep  = [c for c in name if c.isdigit()][0]
if match:
    items = match.groups()
tabstring = str.join(tagstrings)

u_dict = dict.fromkeys(unique, 0)
#u_df = pd.DataFrame.from_dict(u_dict, orient=[int(value) for value in u_dict.values()], 
#                              columns=[str(key) for key in u_dict.keys()])
u_df = pd.DataFrame.from_dict(u_dict, orient='index', columns=['count'])
u_df.to_csv(join(IMDIR, 'u_df.xlsx'))
impaths = [join(allimages[0],category)
           for allimages in os.walk(IMDIR)
           for category in allimages[1]]
counts = [(bname(impath), len(os.listdir(impath)))
          for impath in impaths]
for folder in counts:
    u_dict[folder[0]] += folder[1]
inv = pd.read_excel(INVPATH)
for concept in unique:
    if inv.columns.__contains__(concept) == False:
        print(concept)
#inv.to_excel(join(bname(IMDIR),))
for concept in enumerate(inv.columns):
    if inv.columns.__contains__('inanimate') == True:
        print(concept)
        
def get_en_fr():
    en_allsyns = list(wn.all_synsets())
    en_names = dict(zip([str(s._offset) for s in en_allsyns if s.pos() == 'n'],
                          [(s._lemma_names[0], s._name) for s in en_allsyns if s.pos() == 'n']))
    fr_names = get_fr_n_dict()
    ds = [en_names, fr_names]
    d = {}
    for k in en_names.keys():
      d[k] = flatten(tuple(d[k] for d in ds))
    return d

en_fr = get_en_fr()

def xml_to_json(docpath):
    with open(XMLDOC) as in_file:
        xml = in_file.read()
        with open(join(dname(docpath),'WoNeF.json'), 'w') as out_file:
            json.dump(xmltodict.parse(xml), out_file)