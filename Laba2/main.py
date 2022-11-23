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
    images = img_lookup.find_images(lookup_folder="images")
    print(images)
    for img_path in images:
        print()
        print("Working with image {}".format(img_path))
        filename= img_path.split("/")[-1]
        output_folder = os.path.join("output", filename.split(".")[0])
        if (os.path.exists(output_folder) != True) :
            os.mkdir(output_folder)
        A_labeled_image, A_count = connected_comp.connected_components_from_scratch(filename=img_path, sigma=3.0, t=0.5, connectivity=2)

        fig, ax = plt.subplots()
        plt.imshow(skimage.color.label2rgb(skimage.util.invert(A_labeled_image)))
        plt.axis("off");
        plt.savefig(os.path.join(output_folder, "inverted.jpg"))
        plt.close()

        plt.imshow(skimage.io.imread(img_path))
        plt.axis("off");
        plt.savefig(os.path.join(output_folder, "original.jpg"))
        plt.close()
        
        print('{} objects found'.format(A_count))

        object_perimeters = parameters.objs_perimeter_evaluation(A_labeled_image, A_count)

        parameters.objs_perimeter_evaluation(A_labeled_image, A_count)

        object_areas = parameters.objs_area_evaluation(A_labeled_image, A_count)

        parameters.objs_area_evaluation(A_labeled_image, A_count)

        parameters.objs_compactness_evaluation(object_perimeters,object_areas, A_count)

        parameters.objs_mass_center_evaluation(A_labeled_image, A_count)

        A_objs_params_list = parameters.bind_params(A_labeled_image, A_count)
        print(A_objs_params_list)
        print()
        # JUST WORKAROUND -- NOT NORMAL FLOW
        A_objs_params_list = A_objs_params_list[0:-1]
        print(A_objs_params_list)

        A_objs_cluster_id_param = k_means.k_means(A_objs_params_list, 4)
        print(A_objs_cluster_id_param)
        
        print(A_objs_params_list)

        # A_objs_cluster_id_param = []
        # for param in A_objs_params_list: #objs_params_list
        #     A_objs_cluster_id_param.append(param[-1])

        print(A_objs_cluster_id_param)

        A_label_ids = np.arange(0, A_count)

        for A_label_id in A_label_ids:
            if os.path.exists(os.path.join(output_folder,"labels")) != True:
                os.mkdir(os.path.join(output_folder, "labels"))
            _, _ = plt.subplots()
            plt.imshow(A_labeled_image == A_label_id, cmap="gray")
            plt.axis("off");
            plt.title('Label ID {}'.format(A_label_id))
            plt.savefig(os.path.join(output_folder,"labels" ,"label"+str(A_label_id)+".jpg"))
        plt.close()

        A_label_ids = np.arange(1, A_count)

        for A_label_id in A_label_ids:
            if os.path.exists(os.path.join(output_folder,"clusters")) != True:
                os.mkdir(os.path.join(output_folder, "clusters"))
            _, _ = plt.subplots()
            plt.axis("off");
            plt.imshow(A_labeled_image == A_label_id, cmap="gray")
            plt.title('Cluster ID {}'.format(A_objs_cluster_id_param[A_label_id-1]))
            plt.savefig(os.path.join(output_folder,"clusters", "cluster"+str(A_label_id)+".jpg"))
        plt.close()
        print("saved at {}".format(output_folder))
if __name__ == "__main__":
    main()