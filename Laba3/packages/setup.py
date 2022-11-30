import numpy as np
np.random.seed(1)
from matplotlib import pyplot as plt
import skimage.data
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.transform import resize
import skimage.util 

from os import path
import os

from packages import hopfield_network

def image2vector(img, w=10, h=10):
    # Resize images 
    img = resize(img, (h,w), mode='reflect')
    # Make binary mask
    threshold = threshold_mean(img)
    binary = img > threshold
    # Transfer to bipolar vector
    shift = 2*(binary*1)-1
    flatten = np.reshape(shift, (w*h))
    return flatten


def vector2image(vec):
    dim = int(np.sqrt(len(vec)))
    return np.reshape(vec, (dim, dim))


def make_noised_vector(vector, steps=10):
    per_step_percentage = int(100/steps)
    corrupted_list = []
    for step in range(1,steps+1):
        corrupted = np.copy(vector)
        inv = np.random.binomial(n=1, p=float((per_step_percentage*step)/100), size=len(corrupted))
        for i, v in enumerate(corrupted):
            if inv[i]:
                corrupted[i] = -1 * v
        corrupted_list.append(corrupted)
    return corrupted_list


def plot(render_map, out_path, figsize=(5, 6)):
    for key, value in render_map.items():
        print(f"\tWorking under '{key}'....")
        predicted_out_dir = path.join(out_path, key)
        if not path.exists(predicted_out_dir):
            os.mkdir(predicted_out_dir)
        percent_per_step = float(100/len(value[1]))
        steps = len(value[1])
        data = vector2image(value[0])
        for i, test, predicted in zip(range(1, steps+1), value[1], value[2]):
            test = vector2image(test)
            predicted = vector2image(predicted)
            fig, axarr = plt.subplots(1, 3, figsize=figsize)
            axarr[0].set_title('Train data')
            axarr[0].imshow(data)
            axarr[0].axis('off')
            axarr[1].set_title("Input data")
            axarr[1].imshow(test)
            axarr[1].axis('off')
            axarr[2].set_title('Recognized data')
            axarr[2].imshow(predicted)
            axarr[2].axis('off')

            plt.tight_layout()
            plt.savefig(path.join(predicted_out_dir, f"prediction{i*round(percent_per_step, 0)}.jpg"))
            print(f"\t\tSaved 'prediction{i*round(percent_per_step, 0)}.jpg' at {predicted_out_dir}")
            