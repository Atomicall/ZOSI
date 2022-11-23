import numpy as np
import math
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import skimage.measure
import random
from sklearn.cluster import KMeans

def neighbor(i,j,label):
    # left
    left = label[i-1,j]
    # above
    above = label[i,j-1]
    neighbor_array = [left,above]
    return neighbor_array

def seq_labeling(image):

    m = image.shape[0]  # rows
    n = image.shape[1]  # columns

    label = np.zeros([m,n], dtype=int)
    new = 0

    link = []
    id = 0 # link index also present object number

    # first pass
    for row in range(m):
        for column in range(n):
            
            # no object
            if image[row,column] == [0] :
                label[row, column] = 0
                # l.write(str(int(label[row,column])))
            
            # object
            else : # check neighbor label
                current_neighbor = neighbor(row,column,label)

                # current is new label
                if current_neighbor == [0,0]:
                    new = new + 1
                    label[row, column] = new
                    # l.write(str(int(label[row, column])))

                # neighbor got label
                else :
                    # only one neighbor labeling => choose the large one (the only label)                    
                    if np.min(current_neighbor) == 0 or current_neighbor[0] == current_neighbor[1]:   
                        label[row,column] = np.max(current_neighbor)
                        # l.write(str(int(label[row, column])))

                    else:
                        label[row,column] = np.min(current_neighbor)
                        # l.write(str(int(label[row, column])))
                        if id == 0:
                            link.append(current_neighbor)
                            id = id +1
                            #print(id)
                            #print(link)
                        else:
                            check = 0
                            for k in range(id) :
                                # intersection
                                tmp = set(link[k]).intersection(set(current_neighbor))
                                if len(tmp) != 0 :
                                    link[k] = set(link[k]).union(current_neighbor)
                                    np.array(link)
                                    check = check + 1
                                    #print(link)
                            if check == 0:
                                id = id +1
                                np.array(link)
                                link.append(set(current_neighbor))
        # l.write('\n')

    # second pass
    for row in range(m):
        for column in range(n):
            for x in range(id):
                if (label[row, column] in link[x]) and label[row, column] !=0 :
                    label[row, column] = min(link[x])


    for row in range(m):
        for column in range(n):
            for x in range(id):
                if (label[row, column] == min(link[x])):
                    label[row, column] = x + 1
            #R.write(str(int(label[row, column])))
        #R.write('\n')
    
    # # update file
    # for row in range(m):
    #     for column in range(n):
    #         R.write(str(int(label[row, column])))
    #     R.write('\n')

    # plt.figure(figsize=(30, 10))
    # plt.imshow(label)
    # plt.axis('off')
    # plt.show()
    
    return label, id