import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from sklearn.cluster import KMeans


def n_neighbor(label,row,column,mode=4):
    if mode == 4 :
        neighbor_array = [label[row,column-1],label[row-1,column],label[row,column+1],label[row+1,column]]
    elif mode == 8:
        neighbor_array = [label[row-1,column-1],label[row-1,column],label[row-1,column+1],label[row,column-1],
                          label[row,column+1],label[row+1,column-1],label[row+1,column],label[row+1,column+1]]
    return neighbor_array

def objs_perimeter_evaluation(label, num_obj):

    m = label.shape[0]  # rows
    n = label.shape[1]  # columns

    num = np.zeros(num_obj)

    # calculate object perimeter
    for row in range(m):
        for column in range(n):
            if label[row,column] != 0 :
                if row != 0 and row != m-1 and column != 0 and column != n-1 :
                    for x in range(num_obj):
                        if label[row,column] == x+ 1 :
                            neighbor_array = n_neighbor(label,row,column,mode=8)
                            if min(neighbor_array) !=0 :
                              a = 0
                                #label[row,column] = 0
                                #F.write(str(int(label[row,column])))
                            elif min(neighbor_array) == 0 :
                                #F.write(str(int(label[row,column])))
                                num[x] = num[x] +1
            #F.write(str(int(label[row,column])))
        #F.write('\n')
    return num

def objs_area_evaluation(label, num_obj):

    m = label.shape[0]  # rows
    n = label.shape[1]  # columns

    area = np.zeros(num_obj)

    for row in range(m):
        for column in range(n):
            if label[row,column] != 0 :
                for x in range(num_obj):
                    if label[row,column] == x+1 :
                        area[x] = area[x] +1
    return area

def objs_compactness_evaluation(objs_perimeter, objs_area, num_obj):

    compactness = np.zeros(num_obj)

    for id in range(num_obj):
      perimeter = objs_perimeter[id]
      obj_area = objs_area[id]
      #print(area[id])
      #print(perimeter,area)
      if perimeter!=0 and obj_area!=0 :
          compactness[id] = math.pow(perimeter,2)/obj_area
    return compactness

def objs_mass_center_evaluation(label, num_obj):

    objs_area = objs_area_evaluation(label, num_obj)

    m = label.shape[0]  # rows
    n = label.shape[1]  # columns

    mass_centers = np.zeros(num_obj, dtype="i,i")

    for x in range(m):
        for y in range(n):
            if label[x,y] != 0 :
                for id in range(num_obj):
                    if label[x,y] == id+1 :
                        mass_centers[id][0] += x
                        mass_centers[id][1] += y

    for id in range(num_obj):
      if mass_centers[id][0] != 0 and mass_centers[id][1] != 0:
              mass_centers[id][0] /= objs_area[id]
              mass_centers[id][1] /= objs_area[id]


    return mass_centers

def bind_params(label, num_obj):
    
    params = []

    objs_perimeter_param = objs_perimeter_evaluation(label, num_obj)
    objs_area_param = objs_area_evaluation(label, num_obj)
    objs_compactness_param = objs_compactness_evaluation(objs_perimeter_param, objs_area_param, num_obj)
    objs_mass_center_param = objs_mass_center_evaluation(label, num_obj)

    for id in range(num_obj):
        # if objs_area_param[id] < 100:
        #   continue
        # if objs_perimeter_param[id] < 10:
        #   continue

        params.append([
            round(objs_area_param[id],2), 
            round(objs_perimeter_param[id],2),
            round(objs_compactness_param[id],2), 
            [round(objs_mass_center_param[id][0],2), round(objs_mass_center_param[id][1],2)]
            ])
        
    return params
