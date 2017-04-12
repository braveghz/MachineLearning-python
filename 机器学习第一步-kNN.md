---
title: 机器学习第一步
tags:
- MachineLearning
- python
---

其实从知乎上看到了一个链接[从零开始掌握Python机器学习：十四步教程](https://zhuanlan.zhihu.com/p/25761248) 呐，不过可惜的都是英文....

我先看个中文的学习一下 

## KNN算法

### KNN算法介绍

K最近邻（`k-Nearest Neighbor`，`KNN`）分类算法,测量不同特征值之间的距离进行分类。思想很简单：如果一个样本在特征空间中的k个最相似（即特征空间中最邻近）的样本中的大多数属于某一个类别，则该样本也属于这个类别。

 KNN算法中，所选择的邻居都是已经正确分类的对象。该方法在定类决策上只依据最邻近的一个或者几个样本的类别来决定待分样本所属的类别。由于KNN方法主要靠周围有限的邻近的样本，而不是靠判别类域的方法来确定所属类别的，因此对于**类域的交叉或重叠较多的待分样本集**来说，KNN方法较其他方法更为适合。

该算法在分类时有个主要的不足是，当**样本不平衡**时，如一个类的样本容量很大，而其他类样本容量很小时，有可能导致当输入一个新样本时，该样本的K个邻居中大容量类的样本占多数。因此可以采用权值的方法（和该样本距离小的邻居权值大）来改进。该方法的另一个不足之处是**计算量较大**，因为对每一个待分类的文本都要计算它到全体已知样本的距离，才能求得它的K个最近邻点。目前常用的解决方法是事先对已知样本点进行剪辑，事先去除对分类作用不大的样本。该算法比较适用于样本容量比较大的类域的自动分类，而那些样本容量较小的类域采用这种算法比较容易产生误分。

总的来说就是我们已经存在了一个带标签的数据库，然后输入没有标签的新数据后，将新数据的每个特征与样本集中数据对应的特征进行比较，然后算法提取样本集中特征最相似（最近邻）的分类标签。一般来说，只选择样本数据库中前k个最相似的数据。最后，选择k个最相似数据中出现次数最多的分类。

其算法描述如下：
- 计算已知类别数据集中的点与当前点之间的距离
- 按照距离递增次序排序
- 选取与当前点距离最小的k个点
- 确定前k个点所在类别的出现频率
- 返回前k个点出现频率最高的类别作为当前点的预测分类

### KNN算法--Python实现

> you need to install : python, Numpy, scipy, Matplotlib

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# knn1.py
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
	    # so, classCount.items() = [('A', 2), ('B', 1)]
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

```

测试结果
```python
braveghz@braveghz:~/MachineLearning-python/knn$ python knn1.py 
Your input is: [ 1.2  1. ] and classified to class:  A
Your input is: [ 0.1  0.3] and classified to class:  B
```


#### kNN进阶

用kNN来分类一个大点的数据库，包括数据维度比较大和样本数比较多的数据库。这个数据库包括数字0-9的手写体。每个数字大约有200个样本。每个样本保持在一个txt文件中。手写体图像本身的大小是32x32的二值图，转换到txt文件保存后，内容也是32x32个数字，0或者1。 数据库解压后有两个目录：目录trainingDigits存放的是大约2000个训练数据，testDigits存放大约900个测试数据。

```python
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

```
执行结果
```python
braveghz@braveghz:~/MachineLearning-python/knn$ python knn2.py 
step 1: load data...
---Getting training set...
---Getting testing set...
step 2: training...
step 3: testing...
step 4: show the result...
The classify accuracy is: 98.63%

```



### 参考文献

[机器学习算法与Python实践之（一）k近邻（KNN](http://blog.csdn.net/zouxy09/article/details/16955347)


