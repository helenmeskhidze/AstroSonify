import datareader, config, plotter, sonifier, helpers, midifier
import sys
import numpy as np

class importError(Exception):
    pass

def main():
    print("importing")
    file = config.file
    
    if file.lower().endswith(('.png')): 
        image_data = datareader.pngreader(config.obj)
    elif file.lower().endswith(('.fits')): 
        image_data = datareader.fitsreader(config.obj)
    else:
        raise importError("Not a supported file import type")
    image_data = helpers.normalize_frames(image_data)
    
    # choose to either do audio with midi or fourier 
    midifier.midify_image(image_data)

    # print("plotter called")
    # fig = plotter.visual(image_data) 
    
    # print("sonifier called")
    # sonifier.fourier_sonifier(image_data)
    
    print("merging")
    helpers.combine()

main()