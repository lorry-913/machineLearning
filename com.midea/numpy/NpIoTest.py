#encoding=utf-8
import numpy as np


if __name__ == '__main__':
    data=np.genfromtxt("./data/iris.csv",delimiter=',')


    #处理缺失值
    #1.数据量足够大的情况下直接删除含有缺失值的数据
    #2.数据量比较小用插补法，求其他列的平均值或中位数放进去
    data=data[1:-1,:]#切片 取第二行到最后一行的数据 全列
    print data
    print "特征"
    print data[:,0:4]
    print data[:,0:4].shape

    print "标签"
    print data[:,-1]
    print data[:, -1].shape
    print data[:,-1].transpose()
    print np.matrix(data[:,0:4])#变成矩阵


