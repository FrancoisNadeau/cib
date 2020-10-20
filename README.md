# Courtois-Neuromod Imagebank (CIB)

## Code to inventorize and see stimuli distribution across categories

### load_cib.py

#### Generate nested dictionnairies with "category, total items in category,
#### files in category and saves output to json file 'cib_inv.json'

#### Navigate the database
##### Navigate through categories as normal dict items
###### - A graphic variable explorer such as provided in Spyder is helpful -

## TO-DO

[ ] Complete the 'restaurant', 'house' categories & other places
[ ] Complete the 'tree' 2nd level category
[ ] Validate category distribution asymetries according to either or both:
###### A) Neuronal sources
###### B) Human validated image databases
###### C) Artificially (DNN) validated image datasets
####### - using SUN or COCO datasets?

[ ] Re-implement WN compatibility

####### In Spyder 4.x, wn.synset objects are returned as 'metacontainer' objects,
which use too much space to load them as in previous versions
