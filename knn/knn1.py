#!/usr/bin/python
# -*- coding: UTF-8 -*-

#########################################  
# kNN: k Nearest Neighbors  
  
# Input:      newInput: vector to compare to existing dataset 
#             dataSet:  size m data set of known vectors 
#             labels:   data set labels  
#             k:        number of neighbors to use for comparison   
              
# Output:     the most popular class label  
#########################################  

from numpy import *  
import operator  
  
# create a dataset which contains 4 samples with 2 classes  
def createDataSet():  
    # create a matrix: each row as a sample  
    group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])  
    labels = ['A', 'A', 'B', 'B'] # four samples and two classes  
    return group, labels  
  
# classify using kNN  
def kNNClassify(newInput, dataSet, labels, k):  
    numSamples = dataSet.shape[0] # shape[0] stands for the num of row  
  
    ## step 1: calculate Euclidean distance  
    # tile(A, reps): Construct an array by repeating A reps times  
    # the following copy numSamples rows for dataSet  
    diff = tile(newInput, (numSamples, 1)) - dataSet # Subtract element-wise  
    # for example :newInput is [1.2, 1.0]
    # tile(newInput, (numSamples, 1)) = array([[1.2, 1.0], [1.2, 1.0], [1.2, 1.0], [1.2, 1.0]])
    # so , diff =
    #    [[ 0.2  0.1]
    #     [ 0.2  0.0]
    #     [ 1.1  0.8]
    #     [ 1.2  0.9]]
    squaredDiff = diff ** 2 # squared for the subtract  
    # so ,  squaredDiff = 
    #    [[ 0.04  0.01]
    #     [ 0.04  0.00]
    #     [ 1.21  0.64]
    #     [ 1.44  0.81]]
    squaredDist = sum(squaredDiff, axis = 1) # sum is performed by row  axis = 1:将一个矩阵的每一行向量相加
    # so , squaredDist = [ 0.05  0.04  1.85  2.25]
    distance = squaredDist ** 0.5  
    # so , distance = [ 0.2236068   0.2         1.36014705  1.5       ]
  
    ## step 2: sort the distance  
    # argsort() returns the indices that would sort an array in a ascending order  升序索引
    sortedDistIndices = argsort(distance)   
    classCount = {} # define a dictionary (can be append element)  
    for i in xrange(k):  # k is Function Parameter

        ## step 3: choose the min k distance  
        voteLabel = labels[sortedDistIndices[i]]  
        # voteLabel = A A B

        ## step 4: count the times labels occur  
        # when the key voteLabel is not in dictionary classCount, get() will return 0  
        # dict.get(key, default=None)  key -- 字典中要查找的键。 default -- 如果指定键的值不存在时，返回默认值值。
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1  
    ## step 5: the max voted class will return  
    maxCount = 0  
    for key, value in classCount.items():  
        if value > maxCount:  
            maxCount = value  
            maxIndex = key  
  
    return maxIndex  

def main(): 
  
    dataSet, labels = createDataSet()  
    testX = array([1.2, 1.0])  
    k = 3  
    outputLabel = kNNClassify(testX, dataSet, labels, 3)  
    print "Your input is:", testX, "and classified to class: ", outputLabel  
  
    testX = array([0.1, 0.3])  
    outputLabel = kNNClassify(testX, dataSet, labels, 3)  
    print "Your input is:", testX, "and classified to class: ", outputLabel 

if __name__ == '__main__':
    main()

