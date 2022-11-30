import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from PIL import Image
import os.path as path
import os
import sys

from packages import files_lookup
from packages import argv_parser
from packages import letter_generator
from packages import hopfield_network
from packages import setup


# Option 7 = З,П,Ь
def main():
    parameters = argv_parser.parse(["images_dir", "output_dir", "generate_images", "letter_size", "font_dir"])
    images_dir, out_dir, generate_images, letter_size, font_dir  = parameters
    letter_size = int(letter_size)
    print(parameters)
    if (not path.isdir(images_dir)):
        os.makedirs(images_dir)
    elif generate_images == None: 
        raise Exception("[ERROR] No samples provided!")
    if  not path.exists(out_dir):
        os.makedirs(out_dir)

    if generate_images:
        fonts_list = files_lookup.find_files_by_regex(font_dir, "courier.*\.ttf")
        letters_list = (generate_images).split(",")
        letter_generator.generate_images_from_letters(letters_list, images_dir, fonts_list[0], letter_size, "jpg")

    samples_paths_list = files_lookup.find_files_by_regex(lookup_folder=images_dir, reg_exp=".*\.(jp[e]?g|png)")
    print(parameters, samples_paths_list, sep='\n')

    samples = [ skimage.io.imread(im) for im in samples_paths_list ]

    print("[INFO] Starting preprocessing....")
    samples = [ setup.image2vector(s, h=128 ,w=128) for s in samples ]
    
    noised_samples = [ setup.make_noised_vector(s, 10) for s in samples]

    model = hopfield_network.Hopfield_Network()
    print("[INFO] Starting training weights...")
    model.train_weights(samples)
    print("[INFO] Finished training network!!")
    
    print("[INFO] Start to predict...")
    predicted = model.predict(noised_samples, threshold=0)
    print("[INFO] Finished predicting images!!!")

    print("[INFO] Saving demo plots...")
    render_map = { (path.split("\\")[-1]).split(".")[0] : [s, n, p] for path, s, n, p in zip(samples_paths_list, samples, noised_samples, predicted)}
    setup.plot(render_map, out_path=out_dir)
    print("[INFO] Finished saving demo plots")
    print("[INFO] End of the programm!!!")
    
if __name__ == "__main__":
    main()
