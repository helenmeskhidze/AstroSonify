import config 
import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
from PIL import Image
import PIL
import numpy as np 

def fitsreader(filename): 
    raw_data = astropy.io.fits.open(config.location+"data/"+filename+".fits") 
    raw_data.info
    image_data = raw_data[0].data
    print("successful import")
    return image_data

def pngreader(filename):
    raw_data = Image.open(config.location+"data/"+filename+".png").convert('L')
    image_data = np.array(raw_data)
    print("successful import")
    return(image_data)
    


