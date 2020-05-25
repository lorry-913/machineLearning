#encoding=utf-8
import numpy as np


if __name__ == '__main__':
    a=np.array([1,2,3])
    print a.shape
    print a.dtype
    print a.itemsize
    print a.ndim
    b=np.array([[1,2,4],[2,4,6]])
    print b.shape
    print b.dtype
    print b.itemsize
    print b.ndim
    c=np.array([[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]])
    print c.shape
    print c.dtype
    print c.itemsize
    print c.size
    print c.ndim
    e=np.array([[1,2,3],[2,3,5]],dtype='float64')
    print e.dtype


    f=np.zeros(shape=(3,3),dtype="int32")
    f1=np.ones(shape=(3,3),dtype="float32")
    print f
    print f1

    array=[[1,2],[3,4]]
    print array
    data1=np.array(array)
    data1 = np.array(data1)
    data2 = np.copy(data1)
    data3 = np.asarray(data1)
    data1[0,1]=1000
    print data1
    print data2
    print data3

    aaa=np.linspace(0,10,100)
    print aaa
    ccc=np.arange(0,10,0.1)
    print ccc


