#encoding=utf-8

import numpy as np

#双曲正切函数tanh
def tanh(x):
    return np.tanh(x);

#双曲正切函数求导
def tanh_deriv(x):
    return 1.0-np.tanh(x)*np.tanh(x)

#逻辑斯蒂函数
def logistic(x):
    return 1/(1+np.exp(-x))

def logistic_deriv(x):
    return logistic(x)*(1-logistic(x))

class NeuralNetWork:
    # layers指的是每层内有多少个神经元 layers内的数量表示有几层
    def __init__(self,layers,activation='tanh'):
        if activation == 'logistic':
            self.activation = logistic
            self.activation_deriv = logistic_deriv
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_deriv = tanh_deriv

        self.weight=[]
        #Python len() 方法返回对象（字符、列表、元组等）长度或项目个数。
        for i in range(1,len(layers)-1):
            # 第一句是对当前层与前一层之间的连线进行权重赋值，范围在 -0.25 ~ 0.25之间
            self.weight.append((2 * np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1) * 0.25)
            # 第二句是对当前层与下一层之间的连线进行权重赋值，范围在 -0.25 ~ 0.25之间
            self.weight.append((2 * np.random.random((layers[i] + 1, layers[i + 1])) - 1) * 0.25)

if __name__ == '__main__':
    weight=[]
    layer=[2, 2, 1]
    for i in range(1, len(layer) - 1):
        print i
        # 第一句是对当前层与前一层之间的连线进行权重赋值，范围在 -0.25 ~ 0.25之间
        weight.append((2 * np.random.random((layer[i - 1] + 1, layer[i] + 1)) - 1) * 0.25)
        # 第二句是对当前层与下一层之间的连线进行权重赋值，范围在 -0.25 ~ 0.25之间
        weight.append((2 * np.random.random((layer[i] + 1, layer[i + 1])) - 1) * 0.25)
    # print (2*np.random.random((3,3))-1)*0.25
    print weight

