# Courtois-Neuromod Imagebank (CIB)

## Code to inventorize and see stimuli distribution across categories

### load_cib.py

#### Generate nested dictionnairies with "category, total items in category,
#### files in category and saves output to json file 'cib_inv.json'

#### Navigate the database
##### Navigate through categories as normal dict items
###### - A graphic variable explorer such as provided in Spyder is helpful -
######          - Currently unavailable: Index-value pairs are not yet recognized by pandas
######               - see TO-DO*

## TO-DO
- [_] Make cib_inv.json more readable

- [_] Complete the 'restaurant', 'house' categories & other places

- [_] Complete the 'tree' 2nd level category

- [_] Validate category distribution asymetries according to either or both:
    ##### A) Neuronal sources
    ##### B) Human validated image databases
    ##### C) Artificially (DNN) validated image datasets

- [_] Re-implement WN compatibility
    ##### In Spyder 4.x, wn.synset objects are returned as 'metacontainer' objects.
    ##### This uses too much space to load them in a dataframe as in previous versions.



