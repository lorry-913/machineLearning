#encoding=utf-8
from sklearn import svm
import numpy as np
import sys
import time
from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split


#加载数据返回特征和标签
def loadData(filename):
    data=np.genfromtxt(filename,delimiter=',')
    print data.shape
    x=data[:,:-1]
    y=data[:,-1]
    scaler=StandardScaler()
    x_std = scaler.fit_transform(x)  # 标准化
    x_train, x_test, y_train, y_test = train_test_split(x_std, y, test_size=.3)
    return x_train, x_test, y_train, y_test

def svm_c(x_train, x_test, y_train, y_test):
    # rbf核函数，设置数据权重
    svc = SVC(kernel='rbf', class_weight='balanced', )
    c_range = np.logspace(-5, 15, 11, base=2)
    print c_range
    gamma_range = np.logspace(-9, 3, 13, base=2)
    # 网格搜索交叉验证的参数范围，cv=3,3折交叉
    param_grid = [{'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range}]
    grid = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
    # 训练模型
    clf = grid.fit(x_train, y_train)
    print clf
     # 计算测试集精度
    score = grid.score(x_test, y_test)
    print('精度为%s' % score)


if __name__ == '__main__':
    filename='F:\pyworkspace\machineLearning\com.midea\decisionTree\data\iris.csv'
    x_train, x_test, y_train, y_test=loadData(filename)
    svm_c(    x_train, x_test, y_train, y_test)