#encoding=utf-8
from math import log
import operator
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#读取文件创建数据集,返回数据集和标签
def createDataSet(trainDataFile):
    dataSet=[]
    labels=[]
    index=0
    try:
        fin=open(trainDataFile)
        fileArray=fin.readlines()
        rowSize=len(fileArray)
        colSize=len(fileArray[0].split(","))
        dataSet=np.zeros((rowSize,colSize))
        labels=[example[-1] for example in dataSet]
        for line in fileArray:
            line = line.strip()
            fields = line.split(",")
            dataSet[index, :] = fields[0:colSize]
            index += 1
    except:
        print "路径错误"
        sys.exit()
    return dataSet,labels
#IDE3
def calShannoEnt(dataSet):
    numEntries=len(dataSet)
    lableCounts={}#统计标签出现的次数
    for featVec in dataSet:
        currentLable=featVec[-1]#得到最后一列标签
        if currentLable not in lableCounts:
            lableCounts[currentLable] = 0
        lableCounts[currentLable] += 1
    shannoEnt=0.0
    for key in lableCounts:
        prob = float(lableCounts[key]) / numEntries
        shannoEnt -= prob * log(prob, 2)
    return shannoEnt
# 商越高则混合数据也越高，得到熵之后我们就可以按照最大信息增益方法划分数据集

#根据数据集的特征值划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis+1]
            reducedFeatVec=reducedFeatVec.tolist()
            print type(reducedFeatVec)
            reducedFeatVec.extend(featVec[axis+1:])
            print type(retDataSet)
            retDataSet.append(reducedFeatVec)
    return retDataSet

#得出最佳的特征
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1    #last col is label
    baseEntropy = calShannoEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]#得到四列特征值
        uniqueVals = set(featList)#得到每个特征的唯一特征值
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob *calShannoEnt(subDataSet)    #calc conditional entropy
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount:classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True),
    return sortedClassCount[0][0]

#标签列表包含
def createTree(dataSet,lables):
    classList = [example[-1] for example in dataSet]  # 也可以用numpy获取比如numpy.array([:,-1])
    if classList.count(classList[0]) == len(classList):
        return classList[0]#类别都一样,结束
    if len(dataSet[0])==1:
        return majorityCnt(classList)#只有一个属性，结束
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLable=lables[bestFeat]
    mytree={bestFeatLable:{}}
    del(lables[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLables=lables[:]
        mytree[bestFeatLable][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLables)
    return mytree

'''
信息熵”(information entropy)是度量样本集合纯度的一种常用指标，若集合D中存在d个类别的N个样本，令pk=NkN p_{k}=\frac{N_{k}}{N}p 
 为从集合D中随机选取一个样本属于第k类样本的概率，则有下述信息熵定义：
'''
def calShannonEntOfFeature(dataSet,feat):
    numEntries = len(dataSet)
    labelCounts = {}
    for feaVec in dataSet:
        currentLabel = feaVec[feat]
        if currentLabel not in labelCounts:
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt
    # 商越高则混合数据也越高，得到熵之后我们就可以按照最大信息增益方法划分数据集

if __name__ == '__main__':
    fileName="./data/iris.csv"
    dataSet,lables=createDataSet(fileName)
    createTree(dataSet,lables)