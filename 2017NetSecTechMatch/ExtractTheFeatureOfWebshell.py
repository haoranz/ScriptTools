#! python2
# -*-coding: utf-8-*-
# @Time    : 2017/5/13 14:26
# @Author  : Haoranz
# @Function: Extract the Feature from the WebShell Test Data in "2017 Network Security Tech Match".
# @DataFormat:  000001,n,33c6864d4326dedf678a9f09f69c7381/52d81ff1356b7a2323268a6f8b728473,Action=vy16raSE&status=Tbn

from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('latin-1')  # ('latin-1')
import codecs
import chardet
import UrlValueDecode
import numpy
import re


def main(filePath, typePage, resPath):
    resList = []
    featureList = []
    with codecs.open(filePath, "r+", "latin-1") as fOpen:
        for iLine in fOpen.readlines():
            #Confirm if the No.DATA is to be deal.
            if iLine[:6].isdigit() and int(iLine[:6]) > 0 and int(iLine[:6]) < 300000:
                iList = iLine.split(',', 2)
                if iList[1] in ["n","w"]:
                    del iList[1]
                # Deal with the error that the URL join the Params without ",".
                # [u'1006415', u'http://7de80d4aefc1e8a5c8613465ad1a83ac/f53a5f0a50e14873a18b478ca91592a0/77f76c13b6829c85e129538159f46309/6ed41384a656e358c771812a93e2c3b5ecstoken=david61&password=roy15&_=0.5099432172765691\n']
                if len(iList) == 2:
                    arrIList = []
                    arrIList.append(iList[0])
                    arrTemp = iList[1].split('/')
                    strTemp = ""
                    for i in arrTemp[:-1]:
                        strTemp += i + "/"
                    strTemp += arrTemp[-1][:32]
                    arrIList.append(strTemp)
                    arrIList.append(arrTemp[-1][32:])
                    iList = arrIList

                if len(iList) == 3:

                    # Is this kind of data need to deal.
                    # if iList[1] == typePage:

                    iResList = []
                    iResList.append(iList[0])
                    # iResList.append(iList[1])
                    iResList.append(urlPickup(iList[1]))
                    iResList.append(UrlValueDecode.paramUrlFormat(iList[2].strip()))
                    resList.append(iResList)

                    # featureLine = featureCompose(iResList)
                    # featureList.append(featureLine)

                    try:
                        featureLine = featureCompose(iResList)
                        featureList.append(featureLine)
                    except:
                        featureList.append(featureLine)
                else:
                    print iList

    with open(resPath, 'w') as f:
        for featureLine in featureList:
            # print featureList
            f.write(str(featureLine) + "\n")


def featureCompose(iPrint):
    # 特征列表
    featureList = []
    # 关键词匹配命中结果
    #
    keyWord = ["password", "username", "echo", "$_POST", "base64_decode", "ini_set", "charset", "fopen"]
    keyWordRes = [0, 0, 0, 0, 0, 0, 0, 0]
    featureStr = ""
    # 记录编号
    featureList.append(iPrint[0])
    # 记录类型
    # featureList.append(iPrint[1])
    # 特征1:URL总长度（归一化）
    featureList.append(iPrint[2][-1][0] / 1000 < 1 and iPrint[2][-1][0] / 1000 or 1)
    # 特征2:KeyValue对数
    featureList.append(iPrint[2][-1][1])
    if len(iPrint[2][-1][-1]) > 0:
        # 特征3:Key/Value最大值
        featureList.append(round(numpy.max(iPrint[2][-1][-1]), 5))
        # 特征4:Key/Value最小值
        featureList.append(round(numpy.min(iPrint[2][-1][-1]), 5))
        # 特征5:Key/Value平均值
        featureList.append(round(numpy.mean(iPrint[2][-1][-1]), 5))
        # 特征6:Key/Value标准差
        featureList.append(round(numpy.std(iPrint[2][-1][-1], ddof=1), 5))
        # featureList.append(type(round(numpy.std(iPrint[3][-1][-1], ddof=1), 5)))
    else:
        featureList.append(-1)
        featureList.append(-1)
        featureList.append(-1)
        featureList.append(-1)
    # featureList.append(iPrint[3][:-1])

    # 特征7:大小写字母与数字占比
    # 特征8:是否包含系统路径
    winpath = r'^([a-zA-Z]:|\\\\[a-zA-Z0-9_.$ -]+\\[a-z0-9_.$ -]+)?((?:\\|^)(?:[^\\/:*?"<>|\r\n]+\\)+)'
    lnxPath = r'^/([\w-]+[/])+'
    isOsPath = 0
    for iList in iPrint[2][:-1]:
        for iListStr in iList:
            for xindex in range(0, 8):
                if keyWord[xindex] in iListStr:
                    keyWordRes[xindex] = 1
            if re.match(winpath, iListStr) or re.match(lnxPath, iListStr):
                isOsPath = 1
            featureStr += iListStr.encode(encoding="utf-8")
    # 转换Ascii码
    # 0-9:48-57
    # a-z:97-122
    # A-Z:65-90
    if len(featureStr) > 0:
        normalChar = 0
        for iStr in featureStr:
            asciStr = ord(iStr)
            if (asciStr >= 48 and asciStr <= 57) or (asciStr >= 65 and asciStr <= 90) or (
                            asciStr >= 97 and asciStr <= 122):
                normalChar += 1
        featureList.append(round(normalChar / len(featureStr), 5))
    else:
        featureList.append(-1)

    featureList.append(isOsPath)
    for i in keyWordRes:
        featureList.append(i)
    # featureList.append(keyWordRes)

    return featureList


def strNum(strValue):
    return 'No:' + strValue


def urlPickup(strValue):
    return "URL:" + strValue


if __name__ == '__main__':
    #The Target File Path.
    #filePath = "..\..\TestData\subject2_A\\filelist_A.txt"
    #filePath = "..\..\TestData\subject2_B\\filelist_B.txt"
    filePath = "..\..\TrainingData\web_list.txt"

    #The Output File Path.
    #resultPath = "..\..\TestData\subject2_A\\filelist_A_Feature.txt"
    #resultPath = "..\..\TestData\subject2_B\\filelist_B_Feature.txt"
    resultPath = "..\..\TrainingData\web_list_Feature.txt"
    #Which Kind of Signature to deal with.
    typePage = "n"  # n#w

    main(filePath, typePage, resultPath)
