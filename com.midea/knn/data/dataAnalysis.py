#encoding=utf-8
import operator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def file2matrix(filename):
    fr=open(filename)
    arrayLines=fr.readlines()##读取1000行数据
    size=len(arrayLines)
    returnMat=np.zeros((size,3))#初始化1000行3列0矩阵
    classLableVector=[]
    index=0
    for line in arrayLines:
        line=line.strip()
        lineArray=line.split(",")
        returnMat[index,:]=lineArray[0:3]
        classLableVector.append(int(lineArray[-1]))
        index+=1
    #得到特征（km,game,ice,label）和标签
    return returnMat,classLableVector

#归一化(目的是为了防止较大的特征值对其他的特征值的影响)
#三个特征向量，每年获得的飞行常客里程数 数值很大，所以再求距离的时候对值得影响很大。所以我们需要将这一特征的值转化为0~1之间
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    # 取出每一列的最大值
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    # 创建一个与dataSet 一样大小的矩阵 用0填充
    normDataSet = np.zeros(np.shape(dataSet))
    # 去除data的行数
    m = dataSet.shape[0]
    #tile minVals横行重负m次,列 出现一次
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    # # 归一化特征 newValue = （oldvalue - min)/(max-min)
    normDataSet = normDataSet / np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals



# featureValueArray,lableArray=file2matrix('knnDataSet.txt')
# # fig=plt.figure()
# # ax=fig.add_subplot(111)
# # # ax.scatter(featureValueArray[:,0],featureValueArray[:,1])
# # # ax.scatter(featureValueArray[:,0],featureValueArray[:,2])
# # ax.scatter(featureValueArray[:,1],featureValueArray[:,2])
# #
# # plt.show()
#
# normDataSet, ranges, minVals=autoNorm(featureValueArray)
# print normDataSet
