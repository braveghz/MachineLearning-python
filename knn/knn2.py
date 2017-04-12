#!/usr/bin/python
# -*- coding: UTF-8 -*-
# knn2.py
#########################################  
# kNN: k Nearest Neighbors  
  
# Input:      inX: vector to compare to existing dataset   
#             dataSet: size m data set of known vectors  
#             labels: data set labels  
#             k: number of neighbors to use for comparison   
              
# Output:     the most popular class label  
#########################################  
  
from numpy import *  
import operator  
import os  
  
# classify using kNN  
def kNNClassify(newInput, dataSet, labels, k):  
    numSamples = dataSet.shape[0] # shape[0] stands for the num of row  
  
    ## step 1: calculate Euclidean distance  
    # tile(A, reps): Construct an array by repeating A reps times  
    # the following copy numSamples rows for dataSet  
    diff = tile(newInput, (numSamples, 1)) - dataSet # Subtract element-wise  
    squaredDiff = diff ** 2 # squared for the subtract  
    squaredDist = sum(squaredDiff, axis = 1) # sum is performed by row  
    distance = squaredDist ** 0.5  
  
    ## step 2: sort the distance  
    # argsort() returns the indices that would sort an array in a ascending order  
    sortedDistIndices = argsort(distance)  
  
    classCount = {} # define a dictionary (can be append element)  
    for i in xrange(k):  
        ## step 3: choose the min k distance  
        voteLabel = labels[sortedDistIndices[i]]  
  
        ## step 4: count the times labels occur  
        # when the key voteLabel is not in dictionary classCount, get() will return 0  
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1  
  
    ## step 5: the max voted class will return  
    maxCount = 0  
    for key, value in classCount.items():  
        if value > maxCount:  
            maxCount = value  
            maxIndex = key  
  
    return maxIndex   
  
# convert image to vector  
def  img2vector(filename):  
    rows = 32  
    cols = 32  
    imgVector = zeros((1, rows * cols))   # 1 行 1024 列 全0矩阵
    fileIn = open(filename)  
    for row in xrange(rows):  
        lineStr = fileIn.readline()  
        for col in xrange(cols):  
            imgVector[0, row * 32 + col] = int(lineStr[col])  
  
    return imgVector  
  
# load dataSet  
def loadDataSet():  
    ## step 1: Getting training set  
    print "---Getting training set..."  
    dataSetDir = '/home/braveghz/MachineLearning-python/knn/'  
    trainingFileList = os.listdir(dataSetDir + 'trainingDigits') # load the training set
    # so, testingFileList = 
    #   '6_99.txt', '3_87.txt', '3_180.txt', '2_68.txt', '7_198.txt', '1_56.txt', '2_15.txt', '8_2.txt', '1_104.txt', '0_1.txt', '2_80.txt'......]
    numSamples = len(trainingFileList)  #1934
   
    train_x = zeros((numSamples, 1024))  
    train_y = []  

    for i in xrange(numSamples):  
        filename = trainingFileList[i]  # ex filename = '6_99.txt'
        # get train_x  
        train_x[i, :] = img2vector(dataSetDir + 'trainingDigits/%s' % filename)   #一行一个txt文件
        # get label from file name such as "1_18.txt"  
        label = int(filename.split('_')[0]) # return 1  
        train_y.append(label)  
  
    ## step 2: Getting testing set  
    print "---Getting testing set..."  
    testingFileList = os.listdir(dataSetDir + 'testDigits') # load the testing 
   
    numSamples = len(testingFileList)  
    test_x = zeros((numSamples, 1024))  
    test_y = []  
    for i in xrange(numSamples):  
        filename = testingFileList[i]  
  
        # get train_x  
        test_x[i, :] = img2vector(dataSetDir + 'testDigits/%s' % filename)   
  
        # get label from file name such as "1_18.txt"  
        label = int(filename.split('_')[0]) # return 1  
        test_y.append(label)  
  
    return train_x, train_y, test_x, test_y  
    #      datatset labels   newInput  label
    # 也就是说 train_x 是数据集，每一行是一个txt文件，train_y是对应每一行的label ，test_x是要检验的txt，判断test_y是否和其label相同

# test hand writing class  
def testHandWritingClass():  
    ## step 1: load data  
    print "step 1: load data..."  
    train_x, train_y, test_x, test_y = loadDataSet()  
  
    ## step 2: training...  
    print "step 2: training..."  
    pass  
  
    ## step 3: testing  
    print "step 3: testing..."  
    numTestSamples = test_x.shape[0]  
    matchCount = 0  
    for i in xrange(numTestSamples):  
        predict = kNNClassify(test_x[i], train_x, train_y, 3)  #kNN算出来的label
        if predict == test_y[i]:                               #对比其label
            matchCount += 1  
    accuracy = float(matchCount) / numTestSamples  #比对正确率
  
    ## step 4: show the result  
    print "step 4: show the result..."  
    print 'The classify accuracy is: %.2f%%' % (accuracy * 100)

def main():
    testHandWritingClass()  

if __name__ == '__main__':
    main()