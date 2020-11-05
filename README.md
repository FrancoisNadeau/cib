# Courtois-Neuromod Imagebank (CIB)

## Code to inventorize and see stimuli distribution across categories

### Clone to common directory containing both CIB images and this.


### load_cib.py

#### Generate nested dictionnairies with "category, total items in category,
#### files in category and saves output to json file 'cib_inv.json'

#### Navigate the database
Use the 'read_json' function in 'cib_utils.py' to import 'cib_inv.json'
in a Python IDE as a dict.

##### Navigate through categories as normal dict items
  - A graphic variable explorer such as provided in Spyder is helpful -
    - Currently unavailable: Index-value pairs are not yet recognized by pandas
    - see TO-DO*

##### Database has 5 levels
- From top (animate_beings, objects & places) to last (concept)

## TO-DO
- [_] Make cib_inv.json more readable

- [_] Use COCO and SUN databases to complete the 'places' top category

- [_] Validate category distribution asymetries according to either or both:
    ##### A) Neuronal sources
    ##### B) Human validated image databases
    ##### C) Artificially (DNN) validated image datasets

    - [_] Re-organize categories with less than 20 images into more basic
          classification levels (eg. bird talons all in the same category,
            regardless of bird species)

- [_] Re-implement WN compatibility
    In Spyder 4.x, wn.synset objects are returned as 'metacontainer' objects,
    which are too large to load in a dataframe as in previous versions.
    - [_] Synset disambiguation for items in 'place' category
