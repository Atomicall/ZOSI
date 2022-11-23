import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from sklearn.cluster import KMeans

def get_distance(lhv, rhv):
    index = [0, 1, 2]  # area, perimetr, compactness parameters indexes
    distance = 0
    for i in index:
        distance += pow(lhv[i] - rhv[i], 2)   # removed abs fun
    distance = np.sqrt(distance)
    return distance

def select_new_center(cluster):
    distances_sum = []
    for area in cluster:
        distances = [get_distance(area, el) for el in filter(lambda x: x is not area, cluster)]
        distances_sum.append(sum(distances))
    new_center_id = distances_sum.index(min(distances_sum))
    return cluster[new_center_id]

def k_means(params, k):      # append last but not least param - cluster id
    
    clusters = []

    centers = random.sample(params, k)
    
    tmp = [[1] for i in range(k)]
    change = 1
    while change:
        change = 0
        clusters = [[] for i in range(k)]
        
        for param in params:

            distances = [get_distance(param, center) for center in centers]
            min_dist_id = distances.index(min(distances))
            clusters[min_dist_id].append(param)
        
        centers = [select_new_center(cl) for cl in clusters]

        if tmp != clusters:
            change = 1
        tmp = clusters
    
    
    for i in range(len(clusters)):
        for param in params:
            if param in clusters[i]:
                param.append(i)

    objs_cluster_id_param = []
    for param in params: #objs_params_list
        objs_cluster_id_param.append(param[-1])
    
    return objs_cluster_id_param
