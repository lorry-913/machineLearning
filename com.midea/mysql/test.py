#encoding=utf-8
#coding:utf-8
import TestMysql
import requests
import os
import time
import uuid
import easygui as eg


def mkdir(deviceid):
    path="F:/pic/"+str(deviceid)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"
    else:
        print "---  There is this folder!  ---"
    return path

def downloadPic(url,path):
    try:
        name=url.split("/")[7]
        t = time.time()
        nowTime = int(round(t * 1000))
        path = path + "/" + str(nowTime) + ".jpg"
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print("图片保存成功")
    except:
        print("图片获取失败")

def getpic(deviceid,start_time,end_time):
    connector = TestMysql.MysqlHelper("rr-bp16q700r17zdmy9ffo.mysql.rds.aliyuncs.com", "xmgread2", "xmgread541398542",
                                      "sql_xiaomaigui_test")
    connector.connect()
    sql = "select image from xmg_device_viewimg WHERE deviceid=%s AND addtime>%s AND addtime<%s"
    params = []
    params.append(deviceid)
    params.append(start_time)
    params.append(end_time)
    # 执行
    data = connector.fetchall(sql, params)
    return data



if __name__ == '__main__':
    msg = '美智科技图片拉取程序'
    title = '信息输入界面'
    filenames = ['设备号', '起始时间', '结束时间']
    file_value = []
    file_value = eg.multenterbox(msg, title, filenames)
    print(file_value)
    deviceid = file_value[0]
    print('deviceid', deviceid)
    st = file_value[1]
    print('st', st)
    et = file_value[2]
    print('micseq', et)
    path= mkdir("863867027884657");
    data=getpic("863867027884657","2020-04-28 08:30:00","2020-04-28 18:30:00")
    print data.__len__()
    a=1
    for i in data:
        eg.textbox('执行', '拉取中...', i)
#     downloadPic(i[0],path)
       #     a=a+1
       # print "下载完成"

