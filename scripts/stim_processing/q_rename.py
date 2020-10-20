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
