import math
import operator
import matplotlib.pyplot as plt

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

def calcShannonEnt(dataSet):
    length = len(dataSet)
    lib = {}
    for elem in dataSet:
        key = elem[-1]
        if key not in lib:
            lib[key] = 0
        lib[key] += 1
    H = 0.0
    for key in lib:
        prob = lib[key] / length
        H -= prob * math.log(prob, 2) 
    return H

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] 
            reducedFeatVec.extend(featVec[axis+1:]) 
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    baseH = calcShannonEnt(dataSet)
    bestFeature = -1
    gainH = 0.0

    allFeatures = len(dataSet[0]) - 1
    for i in range(allFeatures):
        uniqueChoice = set([x[i] for x in dataSet])
        featureH = 0.0
        for elem in uniqueChoice:
            splitSet = splitDataSet(dataSet, i, elem)
            prob = len(splitSet) / len(dataSet)
            elemH = calcShannonEnt(splitSet)
            featureH += prob * elemH
        if baseH - featureH > gainH:
            gainH = baseH - featureH
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): 
            classCount[vote] = 0 
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree

decisionNode = dict(boxstyle="sawtooth", fc="0.8") 
leafNode = dict(boxstyle="round4", fc="0.8") 
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType): 
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,
        xycoords='axes fraction',
        xytext=centerPt, textcoords='axes fraction',
        va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode) 
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode) 
    plt.show()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0] 
    secondDict = myTree[firstStr] 
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict': 
            numLeafs += getNumLeafs(secondDict[key])
        else:   
            numLeafs +=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0] 
    secondDict = myTree[firstStr] 
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   
            thisDepth = 1
        if thisDepth > maxDepth: 
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': \
                    {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': \
                    {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0] 
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1] 
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt): 
    numLeafs = getNumLeafs(myTree) 
    getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt) 
    plotNode(firstStr, cntrPt, parentPt, decisionNode) 
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD 
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict': 
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW 
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops) 
    plotTree.totalW = float(getNumLeafs(inTree)) 
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

### 3.3
###
def classify(inputTree,featLabels,testVec): 
    firstStr = list(inputTree.keys())[0] 
    secondDict = inputTree[firstStr] 
    featIndex = featLabels.index(firstStr) 
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:   
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w') 
    pickle.dump(inputTree,fw) 
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename) 
    return pickle.load(fr)