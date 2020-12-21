from numpy import *
import operator
from os import listdir

trans = {'didntLike':1, 'smallDoses':2, 'largeDoses':3}

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]]) 
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    diff = tile(inX, (dataSet.shape[0], 1)) - dataSet
    distance = (diff ** 2).sum(axis=1)**0.5
    sorted_dist = distance.argsort()
    classCount = {}
    for i in range(k):
        indexLabel = labels[sorted_dist[i]]
        classCount[indexLabel] = classCount.get(indexLabel, 0) + 1
    sorted_Ct = sorted(classCount.items(), key=lambda item: item[1], reverse=True)
    return sorted_Ct[0][0]

def file2matrix(filename):
    f = open(filename, 'r')
    rowCount = len(f.readlines())
    returnMat = zeros((rowCount, 3))
    labelVec = []

    f = open(filename, 'r')
    count = 0
    for line in f.readlines():
        line = line.strip()
        returnMat[count, :] = line.split('\t')[0:3]
        labelVec.append(line.split('\t')[-1])
        count += 1
    return returnMat, labelVec

def autoNorm(dataset):
    minVal = dataset.min(0)
    maxVal = dataset.max(0)
    ranges = maxVal - minVal
    normDataset = dataset - tile(minVal, (dataset.shape[0], 1))
    normDataset /= tile(ranges, (dataset.shape[0], 1))
    return normDataset, ranges, minVal

def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        if (classifierResult != datingLabels[i]): 
            errorCount += 1.0
    print(errorCount/float(numTestVecs))

def classifyPerson():
    percentTats = float(input("percentage of time spent playing video games?")) 
    ffMiles = float(input("frequent flier miles earned per year?")) 
    iceCream = float(input("liters of ice cream consumed per year?")) 

    datingDataMat, datingLabels = file2matrix('datingTestSet.txt') 
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    
    print(classifierResult)

def img2vector(filename):
    f = open(filename, 'r')
    vect = zeros((1,1024))
    for i in range(32):
        line = f.readline()
        line = line.strip()
        for j in range(32):
            vect[0, i*32+j] = int(line[j])
    return vect

def handWritingClassTest():
    files = listdir('trainingDigits')
    labels = [x[0] for x in files]

    m = len(files)
    mat = zeros((m, 1024))
    for i in range(m):
        mat[i, :] = img2vector('trainingDigits/{}'.format(files[i]))
    
    errorCount = 0.0
    k = 3

    files = listdir('testDigits')
    n = len(files)
    for i in range(n):
        testInput = img2vector('testDigits/{}'.format(files[i]))
        testOuput = classify0(testInput, mat, labels, k)
        if testOuput != files[i][0]:
            errorCount += 1.0

    print(errorCount / n)