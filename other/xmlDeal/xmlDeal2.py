#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     xmlDeal
   Description :
   Author :        hayden_huang
   Date：          2018/12/28 17:34
-------------------------------------------------
"""

import gzip
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import random

# filename = 'TD-LTE_MRO_HUAWEI_010217007069_409720_20181122000000.xml'

def deal(filename,justfileName):

    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement

    eNBList = collection.getElementsByTagName("eNB")
    # print(eNB)
    for myeNB in eNBList:
        measurementList = myeNB.getElementsByTagName("measurement")
        for mymeasurement in measurementList:
            smrList = mymeasurement.getElementsByTagName("smr")
            myvList = mymeasurement.getElementsByTagName("v")
            # print(len(smrList))
            for mysmr in smrList:
                smrStr = mysmr.childNodes[0].data
                print(smrStr)
                if 'MR.LteScRSRP' in smrStr:
                    for myv in myvList:
                        myvData = myv.childNodes[0].data
                        # print(myvData)
                        split_list = myvData.split(' ')
                        try:
                            first = int(split_list[0])
                        except:
                            continue
                        if first < 31:
                            replacenum = str(random.randint(35,50))
                        else:
                            replacenum = str(first)
                        save_res = replacenum+' '+' '.join(split_list[1:])
                        save_res = save_res.strip()
                        # print(save_res)
                        myv.childNodes[0].data = save_res
                elif 'MR.LteScPlrULQci1' in smrStr:
                    for myv in myvList:
                        myvData = myv.childNodes[0].data
                        # print(myvData)
                        split_list = myvData.split(' ')
                        try:
                            first = int(split_list[0])
                        except:
                            continue
                        if first > 10:
                            replacenum = str(random.randint(2,8))
                        else:
                            replacenum = str(first)
                        save_res = replacenum+' '+' '.join(split_list[1:])
                        save_res = save_res.strip()
                        # print(save_res)
                        myv.childNodes[0].data = save_res

    mysaveFile = os.path.join('newXml', justfileName)
    fb = open(mysaveFile,'w')
    DOMTree.writexml(fb, encoding='utf-8')
    fb.close()



def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    #获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    #创建gzip对象
    open(f_name, "wb+").write(g_file.read())
    g_file.close()


def start():
    file_dir = 'gzdir'
    for root, dirs, files in os.walk(file_dir):
        # print(root)
        # print(dirs)
        # print(files)
        for file in files:
            if os.path.splitext(file)[1] == '.gz':
                print('正在解压：'+file)
                uzfileName =os.path.join(file_dir, file)
                un_gz(uzfileName)

    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.xml':
                print('正在处理：'+file)
                xmlDicName =os.path.join(file_dir, file)
                deal(xmlDicName,file)

    #压缩文件
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.xml':
                print('正在压缩：'+file)
                src = 'newXml/'+file
                dst = 'newXml/'+file+'.gz'
                gZipFile(src, dst)

def gZipFile(src, dst):
    fin = open(src, 'rb')
    fout = gzip.open(dst, 'wb')

    in2out(fin, fout)


def in2out(fin, fout):
    BufSize = 1024 * 8
    while True:
        buf = fin.read(BufSize)
        if len(buf) < 1:
            break
        fout.write(buf)

    fin.close()
    fout.close()

if __name__ == '__main__':
    start()