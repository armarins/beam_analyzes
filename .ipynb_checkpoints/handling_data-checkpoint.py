def get_info_from_directory(dirname_= None, freq_unit="MHz", map_division="bins"):
    import numpy as np
        #formatting: [NSIDE]_[MINfreq]_[MAXfreq]MHZ_[NUMbins]bins
    fmt = dirname_.split("_")
    return {"NSIDE":int(fmt[0]),
            "frequency":{"min":int(fmt[2]),"max":int(fmt[3].split(freq_unit)[0])},
            map_division:int(fmt[4].split(map_division)[0])
           }
def getmap(dirpath_=None, mapname_=None, healpix_readingformat=True):
    import numpy as np
    import healpy as hp
    if healpix_readingformat:
        maps = hp.read_map(os.path.join(dirpath_,mapname_))
    else:
        import astropy.io.fits as fits
        with fits.open(os.path.join(dirpath_,mapname_)) as h:
            maps = h[0].data
    return maps
def get_filenames(dirpath_=None):
    import numpy as np    
    names = np.array([], dtype=np.str)
    for i,iname in enumerate(os.listdir(dirpath_)):
        if "fits"==iname.split(".")[1]:
            names = np.hstack((names,iname))
    return names
def building_cubemaps(dirpath_=None, dirname_=None, healpix_readingformat=True):
    import numpy as np
    import healpy as hp    
    from copy import deepcopy as dcopy
    dirpath_ = os.path.join(dirpath_,dirname_)
    names = get_filenames(dirpath_)
    infos = get_info_from_directory(dirname_)
    #creating a cube to fill in
    HImaps = np.ones((infos['bins'],12*(infos['NSIDE'])**2))
    
    for i,iname in enumerate(names):
        numname = int(iname.split(".fits")[0].split('z')[1])-1 #names in z between 1-30, but cube between 0-29 numeration
        imap = getmap(dirpath_, iname, healpix_readingformat)
        HImaps[numname,:] = dcopy(imap)
    return HImaps