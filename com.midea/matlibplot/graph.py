#encoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cbook as cbook

from BalenceTree import tree

from scipy.interpolate import spline
#mat -matrix矩阵
#     二维数组-二维图标
#plot - 画图
#lib - library

def getSchedulerTree(fileName):
    y1_last = 1.0;
    y2_last = 1.0;
    y3_last = 1.0;
    y4_last = 1.0;
    start = 1
    scheduler_list = [];
    with open(fileName) as file_object:
        lines = file_object.readlines()
    for line in lines:
        index=int(line.split(";")[0].split(":")[1])
        instruct=line.split(";")[1].split(":")[1]
        if float(instruct)==0.0:
            instruct=1.0
        if index==0:
            scheduler_list.append({"big":(float(instruct)-y1_last)/y1_last})
            y1_last=float(instruct)
        if index==1:
            scheduler_list.append({"small":(float(instruct)-y2_last)/y2_last})
            y2_last=float(instruct)

        if index==2:
            scheduler_list.append({"small":(float(instruct)-y3_last)/y3_last})
            y3_last=float(instruct)

        if index==3:
            scheduler_list.append({"small":(float(instruct)-y4_last)/y4_last})
            y4_last=float(instruct)
        start=start+1

        if start%3==0:
            # print "源数据："+str(scheduler_list)
            t = tree()
            t.create_tree(0, scheduler_list)
            print t.middle()
            scheduler_list=[]

            # t.create_tree(0,scheduler_list)
            # print t.middle()





def getData(fileName):
    x=[];y1=[];y2=[];y3=[];y4=[];
    y1_last=0.0;y2_last=0.0;y3_last=0.0;y4_last=0.0
    time = 0
    start=1
    with open(fileName) as file_object:
        lines = file_object.readlines()
    for line in lines:
        scheduler_list = [];
        index=int(line.split(";")[0].split(":")[1])
        instruct=line.split(";")[1].split(":")[1]
        if start%3==0:
            t = tree()
        if index==0:
            y1.append(float(instruct))
        if index==1:
            y2.append(float(instruct))
        if index==2:
            y3.append(float(instruct))
        if index==3:
            y4.append(float(instruct))
        start=start+1
        time = time + 1
    return x,y1,y2,y3,y4


def zhexiantu(x,y1,y2,y3,y4):
    #1.创建画布   长是20，宽是8
    plt.figure(figsize=(20,20))

    #2.绘制折线图
    # plt.plot([1, 2, 3, 4, 5, 6, 7], [17, 17, 18, 15, 11, 11, 13])
    # plt.plot([1,2,3,4,5,6,7],[17,17,18,15,11,11,13])

    #线条说明
    plt.title('RADIX Run Analysis')


    # plt.plot(x, y1, color='green', label='big')
    # plt.plot(x, y2, color='red', label='small1')
    # plt.plot(x, y3, color='blue', label='small2')
    # plt.plot(x, y4, color='yellow', label='small3')
    x=np.array(x)
    y=np.array(y1)
    # 画曲线
    x_new = np.linspace(x.min(), x.max(), 300)
    y_smooth = spline(x, y1, x_new)
    plt.plot(x_new, y_smooth, c='black',label='big')
    plt.plot(x_new, spline(x, np.array(y2), x_new), c='red',label='small_1')
    plt.plot(x_new, spline(x, np.array(y3), x_new), c='blue', label='small_2')
    plt.plot(x_new, spline(x, np.array(y4), x_new), c='yellow', label='small_3')



    plt.legend()  # 显示图例

    # 横坐标
    plt.xlabel('cycle')
    plt.ylabel('instructions')
    plt.savefig("./RADIX2_picture")
    plt.show()

def zhexiantu2():
    plt.figure(figsize=(20, 8))
    x_=range(60)#0-59的数组
    dots=[random.uniform(10,15) for i in x_]# 0-59数组每个元素换成10-15的玩意
    dots2 = [random.uniform(9,13) for i in x_]
    #显示图例不仅lable要加 还要legend
    plt.plot(dots,color='r',label='ShangHai')
    plt.plot(dots2, color='y', label='Beijing')
    plt.legend()

    #
    #添加x，y刻度
    plt.yticks(range(20))
    plt.xlabel("time")
    plt.ylabel("temp")

    #添加网格显示  阿尔法透明度
    plt.grid(True,linestyle="--",alpha=0.5)
    plt.title("picture of temp")
    plt.show()

def zhuzhuangtu():
    '''
       柱状图
    '''
    num = [1, 2, 4, 8]
    times = [9.16, 9.93, 10.17, 11.41]
    plt.bar(range(len(num)), times, color='r', tick_label=num, label='Stanbark')
    plt.xlabel("number of thread")
    plt.ylabel("time")
    plt.show()

def mul_graph():
    plt.subplot(2,2,1)
    num = [1, 2, 4, 8]
    times = [9.16, 9.93, 10.17, 11.41]
    plt.bar(range(len(num)), times, color=['r','g','b', 'c'], tick_label=num, label='Stanbark')
    plt.xlabel("number of thread\n a) FFT")
    plt.ylabel("time(s)")
    plt.subplot(2, 2, 2)
    num = [1, 2,4,8]
    times = [5.14, 5.06, 4.38, 6.50]
    plt.bar(range(len(num)), times, color=['r','g','b', 'c'], tick_label=num, label='Stanbark')
    plt.xlabel("number of thread\nb) RADIX")
    plt.ylabel("time(s)")
    plt.subplot(2, 2, 3)
    num = [1, 2,3,4, 8]
    times = [44.54, 28.82,24.26, 21.48, 26.21]
    plt.bar(range(len(num)), times, color=['r','g','y','b', 'c'], tick_label=num, label='Stanbark')
    plt.xlabel("number of thread\nc) FMM")
    plt.ylabel("time(s)")
    plt.subplot(2, 2, 4)
    num = [1, 2,3,4, 8]
    times = [50.58, 46.28, 44.96,45.31, 53.22]
    plt.bar(range(len(num)), times,color=['r','g','y','b', 'c'], tick_label=num, label='Stanbark')
    plt.xlabel("number of thread\nd) CHOLESKY")
    plt.ylabel("time(s)")
    plt.savefig("./mul_picture")
    plt.show()

def qipao():
    with cbook.get_sample_data('goog.npz') as datafile:
        price_data = np.load(datafile)['price_data'].view(np.recarray)
    price_data = price_data[-250:]  # get the most recent 250 trading days
    delta1 = np.diff(price_data.adj_close) / price_data.adj_close[:-1]
    # Marker size in units of points^2
    volume = (15 * price_data.volume[:-2] / price_data.volume[0]) ** 2
    close = 0.003 * price_data.close[:-2] / 0.003 * price_data.open[:-2]
    fig, ax = plt.subplots()
    ax.scatter(delta1[:-1], delta1[1:], c=close, s=volume, alpha=0.5)
    ax.set_xlabel(r'$\Delta_i$', fontsize=15)
    ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=15)
    ax.set_title('Volume and percent change')
    ax.grid(True)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    mul_graph();
    # mapping_list = [1, 3, 2, 0]
    # # # for core_id, mapping_id in enumerate(mapping_list):
    # # #     print core_id
    # # #     print mapping_id
    # # #     print "--------"
    # #
    # list=[2,5,6,7]
    # print zip(mapping_list, list)
    # # 括号内容相减
    # print any(map(lambda c: abs(int(c[0]) - int(c[1])),
    #     zip(mapping_list, list)))
    # # for f,s in zip(mapping_list,list):
    # #     print f,s



    # list=[{"0":1},{"2":1},{"3":1}];
    # print list[0].keys()
    # print list[0].values()
    # getSchedulerTree("./cholesky.txt")
    # x, y1, y2, y3, y4=getData("./dataSub.txt")
    # x1=[];
    # for i in range(1,y1.__len__()+1):
    #     x1.append(i)
    # zhexiantu(x1, y1, y2, y3, y4)
