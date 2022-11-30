import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from sklearn.cluster import KMeans
import os.path

from . import labeling

def connected_components_from_scratch(output_folder, filename, sigma=1.0, t=0.5, connectivity=2):
    
    # load the image
    image = skimage.io.imread(filename)
    
    # convert the image to grayscale
    gray_image = skimage.color.rgb2gray(image)
    #gray_image = skimage.util.img_as_ubyte(gray_image)
    
    fig, ax = plt.subplots()
    plt.imshow(gray_image)
    plt.axis("off")
    plt.savefig(os.path.join(output_folder, "gray.jpg"))
    plt.close()
    
    # denoise the image with a Gaussian filter
    blurred_image = skimage.filters.gaussian(gray_image, sigma=sigma)
    #blurred_image = skimage.util.img_as_ubyte(blurred_image)
    #blurred_image = gray_image
    #print(blurred_image)

    fig, ax = plt.subplots()
    plt.imshow(blurred_image)
    plt.axis("off")
    plt.savefig(os.path.join(output_folder, "blurred.jpg"))
    plt.close()
    
    # mask the image according to threshold
    #binary_mask = blurred_image < t
    #binary_mask = otsu(blurred_image)

    thr = skimage.filters.threshold_otsu(blurred_image)
    binary_mask = blurred_image < thr
    
    fig, ax = plt.subplots()
    plt.imshow(binary_mask)
    plt.axis("off")
    plt.savefig(os.path.join(output_folder, "binary_mask.jpg"))
    plt.close()
    
    # perform connected component analysis
    inverted_binary_mask = skimage.util.invert(binary_mask)
    labeled_image, count = labeling.seq_labeling(inverted_binary_mask)

    return labeled_image, count