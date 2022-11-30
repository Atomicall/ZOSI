import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from sklearn.cluster import KMeans
from PIL import Image
import os.path
import os

from obj_detection import connected_comp
from obj_detection import k_means
from obj_detection import labeling
from obj_detection import parameters
from file_search import img_lookup

def main():
    lookup_folder="images"
    images = img_lookup.find_images(lookup_folder)
    print("Found in folder '{}' files : {}".format(lookup_folder,images))

    for img_path in images:
        print("Working with image {}".format(img_path))
        filename= img_path.split("/")[-1]
        output_folder = os.path.join("output", filename.split(".")[0])
        if (os.path.exists(output_folder) != True) :
            os.mkdir(output_folder)
        A_labeled_image, A_count = connected_comp.connected_components_from_scratch(output_folder, filename=img_path, sigma=3.0, t=0.5, connectivity=2)

        _, _ = plt.subplots()
        plt.imshow(skimage.color.label2rgb(skimage.util.invert(A_labeled_image)))
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, "labled.jpg"))
        plt.close()

        plt.imshow(skimage.io.imread(img_path))
        plt.axis("off")
        plt.savefig(os.path.join(output_folder, "original.jpg"))
        plt.close()
        
        print('{} objects found'.format(A_count))

        A_objs_params_list = parameters.bind_params(A_labeled_image, A_count)
        A_objs_cluster_id_param = k_means.k_means(A_objs_params_list, 4)
        index = 0
        for obj in A_objs_params_list :
            print(
    """Object {a} :  
        area : {b},
        perimetr : {c},
        compactness: {d},
        mass_center: {e}, 
        cluster_id : {f}""".format(a=index, b=obj[0], c=obj[1], d=obj[2], e=obj[3], f=A_objs_cluster_id_param[index])
            )
            index+=1

        A_label_ids = np.arange(0, A_count)

        for A_label_id in A_label_ids:
            if os.path.exists(os.path.join(output_folder,"labels")) != True:
                os.mkdir(os.path.join(output_folder, "labels"))
            _, _ = plt.subplots()
            plt.imshow(A_labeled_image == A_label_id, cmap="gray")
            plt.axis("off")
            plt.title('Label ID {}'.format(A_label_id))
            plt.savefig(os.path.join(output_folder,"labels" ,"label"+str(A_label_id)+".jpg"))
        plt.close()

        A_label_ids = np.arange(1, A_count)

        for A_label_id in A_label_ids:
            if os.path.exists(os.path.join(output_folder,"clusters")) != True:
                os.mkdir(os.path.join(output_folder, "clusters"))
            _, _ = plt.subplots()
            plt.axis("off")
            plt.imshow(A_labeled_image == A_label_id, cmap="gray")
            plt.title('Cluster ID {}'.format(A_objs_cluster_id_param[A_label_id-1]))
            plt.savefig(os.path.join(output_folder,"clusters", "cluster"+str(A_label_id)+".jpg"))
        plt.close()
        print("saved at {}".format(output_folder))



if __name__ == "__main__":
    main()