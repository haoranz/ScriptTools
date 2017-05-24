#! python2
# -*-coding: utf-8-*-
# @Time    : 2017/5/13 14:26
# @Author  : Haoranz
# @Function: Convert encoded URL to decoded key&value. Supported decoding methods include Based64, URLencode or both.

import base64
import urllib
import chardet

def paramUrlFormat(strValue):

    featureList = []
    resKeyValue = []
    keyValueList = strValue.split('&')
    for keyValue in keyValueList:
        fKeyValue = keyValue.split('=',1)
        if len(fKeyValue) > 1:
            kvList = []
            fKeyValueK = fKeyValue[0]
            # fKeyValue[1] = fKeyValue[1].
            # If Value is digit, No decode operation.
            try:
                float(fKeyValue[1])
                fKeyValueV = fKeyValue[1]
            except:
                if fKeyValue[1].isalpha() and fKeyValue[1].islower() and len(fKeyValue[1]) % 4 != 0:
                    fKeyValueV = fKeyValue[1]
                else:
                    fKeyValueV = paramValueDecode(fKeyValue[1])
            kvList.append(fKeyValueK)
            kvList.append(fKeyValueV)

            resKeyValue.append(kvList)
    lenStrValue = 0
    lenListValue = len(resKeyValue)
    keyValueScale = []
    for eachKV in resKeyValue:
        lenStrValue += len(str(eachKV[0]))
        lenStrValue += len(str(eachKV[1]))

        try:
            if len(str(eachKV[1])) == 0:
                keyValueScale.append(round(float(len(str(eachKV[0]))), 3))
            else:
                keyValueScale.append(round(float(len(str(eachKV[0]))) / len(str(eachKV[1])), 3))
        except Exception as e:
            # print str(fKeyValueK)+"  "+str(fKeyValueV)
            # print e
            pass
    featureList.append(len(strValue))
    featureList.append(lenListValue)
    featureList.append(keyValueScale)
    resKeyValue.append(featureList)
    return resKeyValue


def paramValueDecode(str_value):
    res = valueDecode(str_value)
    # print str_value
    try:
        conRes = chardet.detect(res)["confidence"]
    except:
        return str_value
    else:
        if conRes > 0.8:
            # print "FirstResult: "+res
            if res == valueDecode(res):
                return res
            else:
                return paramValueDecode(res)
        else:
            return str_value


def urlDecode(str_value):
    try:
        res = urllib.unquote(str_value)
        # print "1:"+res
        return res
    except Exception as e:
        pass
        # else:
        # print "URL Decode Finished."


def decode_base64(str_value):
    missing_padding = 4 - len(str_value) % 4
    if missing_padding:
        str_value += '=' * missing_padding
    try:
        res = base64.decodestring(str_value)
        # print "2:"+res
        return res
    except Exception as e:
        pass


def valueDecode(str_value):
    if "%" in str_value:
        res_url = urlDecode(str_value)
        if res_url != str_value and res_url:
            # print "3:\n"+res_url+"\n"+str_value
            return res_url
        else:
            return str_value
    elif decode_base64(str_value):
        return decode_base64(str_value)
    else:
        return str_value


if __name__ == '__main__':
    str_value = "%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a%e5%85%85%e5%80%bc%e5%8d%a1"
    # print str_value
    # try:
    #     print base64.decodestring(str_value)
    #     print len(base64.decodestring(str_value))
    # except Exception as e :
    #     print e
    res = paramValueDecode(str_value)
    print "####################"
    print res
