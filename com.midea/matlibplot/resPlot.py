# enccding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cbook as cbook




def getbili(matrix):
    ll = [[0 for i in range(7)] for i in range(8)]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            ll[i][j]=(matrix[i][j]-matrix[i][0])/matrix[i][0]+1
    return ll

def getres(matrix):
    plt.figure(figsize=(10, 8), dpi=80)
    lable = ['fft', 'radiosity', 'fmm',"cholesky","barnes","raytrace","volrend","radix","avg"]
    time = [1.0, 1.0, 1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    ints = [1.072992700729927,0.975103734439834, 0.8281723325479636, 1.2,0.9776247848537005,0.7842323651452281,1.0207612456747406,0.933920704845815,0.9741009835296511]
    my=[0.7372262773722627,0.8070539419087137,0.5368562773476944,0.9232323232323233, 0.764199655765921,0.8609958506224067,1.0397923875432524,0.8854625550660792,0.8193524086073316
]
    x = range(len(lable))

    # plt.bar("equal_time",x, time, width=0.2,label='Stanbark')
    # plt.bar("equal_instructions",[i + 0.2 for i in x], ints, width=0.2,label='Stanbark')
    # plt.bar("propose",[i + 0.4 for i in x], my, width=0.2,label='Stanbark')
    plt.bar(x, time, width=0.2, label='equal_time')
    plt.bar([i + 0.2 for i in x], ints, width=0.2, label='equal_instructions')
    plt.bar([i + 0.4 for i in x], my, width=0.2, label='propose')
    plt.xticks([i + 0.15 for i in x], lable,fontsize=10)
    plt.ylabel("proportion")
    # show lebal equal_time
    plt.legend()
    plt.show()

if __name__ == '__main__':
    list1=[[2.74,2.94,2.02],[59.42,49.21,31.90],[4.95,5.94,4.57],[5.81,5.68,4.44],[4.82,3.78,4.15],[5.78,5.9,6.01],[2.27,2.12,2.01],[4.82,4.70,3.89]]
    # # print getbili(list1)
    getres(getbili(list1))
    # l=[0.7372262773722627,0.5368562773476944,0.9232323232323233, 0.764199655765921,0.8609958506224067,1.0397923875432524,0.8854625550660792,0.8070539419087137]
    # print np.array(l).mean()
