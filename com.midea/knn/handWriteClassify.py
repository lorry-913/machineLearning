#encoding=utf-8
import operator
import numpy as np
import sys
import time
from os import listdir
import datetime

#文本向量化 32x32 -> 1x1024
def img2vector(filename):
    returnVect=np.zeros((1,1024))
    fr=open("./data/trainingDigits/"+filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=lineStr[j]
    return returnVect

#从文件名中解析分类数字
def classnumCut(fileName):
    fileString=fileName.split('.')[0]
    classNumStr = int(fileString.split('_')[0])
    return classNumStr


def trainingDataSet():
    hwLabels = []
    trainingFileList = listdir('./data/trainingDigits')           #获取目录内容
    m = len(trainingFileList)
    trainingMat = np.zeros((m,1024))                          #m维向量的训练集
    for i in range(m):
        fileNameStr = trainingFileList[i]
        hwLabels.append(classnumCut(fileNameStr))
        trainingMat[i,:] = img2vector(fileNameStr)
    return hwLabels,trainingMat

def classify(inX,dataSet,lables,k):
    dataSetSize=dataSet.shape[0]
    diffMat=np.tile(inX,(dataSetSize,1))-dataSet#每个向量对应坐标相减
    sqDiffMat=diffMat**2#向量平方
    sqDistances=sqDiffMat.sum(axis=1)#求和
    distances=sqDistances**0.5#开方
    sortDistance=distances.argsort()#排序
    # print sortDistance
    classCount={}
    for i in range(k):
        votelable=lables[sortDistance[i]]
        # print votelable
        classCount[votelable]=classCount.get(votelable,0)+1
        # print classCount[votelable]
    # b=classCount.iteritems()
    # print list(b)
    # iteritems()方法在需要迭代结果的时候使用最适合，而且它的工作效率非常的高。
    # 以数组第二个元素进行倒叙
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

if __name__ == '__main__':
    starttime = time.time()
    lables, trainingData=trainingDataSet()
    inputImg=img2vector("8_4.txt")
    result=classify(inputImg,trainingData,lables,5)
    endtime = time.time()
    print "识别为：",result
    print "时间：",endtime-starttime
