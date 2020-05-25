#encoding=utf-8
import operator
import numpy as np
import sys
import data.dataAnalysis as da


reload(sys)
sys.setdefaultencoding("utf-8")


'''
classify4个参数：用于分类的输入向量是inX，输入的训练样本级为dataSet,
标签向量为lables,最后参数K标识用于选择最近邻居的数目
核心公式 欧氏距离
'''



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

#10%的数据测试集
def datingClassTest():
    hoRation = 0.4
    datingDataMat,datingLabels = da.file2matrix('data/shiyan.txt')
    norMat,ranges,minVals = da.autoNorm(datingDataMat)
    m = norMat.shape[0] # 总数据1000行
    numTestVecs = int(m*hoRation) # 测试数据100行
    errorCount = 0.0
    for i in range(numTestVecs):
        # norMat[i,:]表示矩阵的切片，i表示测试数据为第i行， ： 表示所有列
        # notMat[numTestVecs:m,:]  ，表示 从 100行到1000行 为训练数据 ，没测试一次都要训练一遍
        classifierResult = classify(norMat[i,:],norMat[numTestVecs:m,:],datingLabels[numTestVecs:m],4)
        print("分类标签: %d,实际标签:%d"%(classifierResult,datingLabels[i]))
        if(classifierResult !=datingLabels[i]):errorCount +=1.0
        print("错误率 : %f" % (errorCount/float(numTestVecs)))

if __name__ == '__main__':
    datingClassTest()