#-*- coding:utf-8 -*-
#字符串乱码问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import datetime
from bs4 import BeautifulSoup
import ConfigParser
import base64
import hashlib

'''
张江人才公寓排序程序
爬虫爬取当前排名
按照之前规律推算大概能排到的日期
haoranz@2017.2.9
配置文件为同目录下的"zj-conf.ini"
'''

class confini(object):
	config = ConfigParser.ConfigParser()
	config.readfp(open("zj-conf.ini", "rb"))
	conArr = config.items("global")
	md5 = hashlib.md5()
	md5.update(conArr[3][1])

	year = int(conArr[0][1].split("-")[0])
	month = int(conArr[0][1].split("-")[1])
	day = int(conArr[0][1].split("-")[2])
	num = int(conArr[1][1])
	username = conArr[2][1]
	pw_bs64 = base64.b64encode(conArr[3][1])
	pw_md5 = md5.hexdigest()

def main():
	wait_remain = get_wait_remain_spider()	#获取剩余排名
	exp_calculate(wait_remain)	#进行预期计算
	
def exp_calculate(wait_remain):
	#调用函数传入剩余排名，若没有则进行手动输入
	if not wait_remain:
		print u"\n获取实时数据失败，请手动输入排名数字\n"
		wait_remain = int(raw_input("Input the Remain:"))
	day_start = datetime.datetime(confini.year,confini.month,confini.day)
	day_now = datetime.datetime.now()
	last_days = (day_now-day_start).days
	day_expect = day_now+datetime.timedelta(days=(wait_remain*last_days/(confini.num-wait_remain)))

	#print '\nStill is:'+str(wait_remain)
	print u'\n按进度可能的排到时期为：'+day_expect.strftime('%Y-%m-%d')
	print u'\n每天大概能前进这些名额：'+str(round((float(confini.num-wait_remain))/last_days,2))
	#print 'Today is:'+day_now.strftime('%Y-%m-%d')
	raw_input('\nPress Enter to exit...')

def get_wait_remain_spider():
	#爬虫爬取页面内容，返回剩余排名

	s = requests.Session()
	#获取Cookie链接&登录链接&获取数据的链接
	url_get_cookie = "http://www.zj-talentapt.com/Default.aspx?InternalLogin=1"
	url_login = "http://www.zj-talentapt.com/Login.aspx?flag=0&userName="+confini.username+"&passWord="+confini.pw_bs64+"&md5="+confini.pw_md5
	url_result = "http://www.zj-talentapt.com/System/WaitingRecord.aspx"
	
	headers = {
		"Host": "www.zj-talentapt.com",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent":" Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":" gzip, deflate, sdch",
		"Accept-Language":" zh-CN,zh;q=0.8"		
	}

	#获取登录Cookie
	cookieRequest = requests.Request('GET', url_get_cookie,headers=headers).prepare()
	res0 = s.send(cookieRequest)
	res0_cookies = requests.utils.dict_from_cookiejar(res0.cookies)	#cookiejar转换成普通Cookie格式
	#s.cookies = res0_cookies

	#Get请求完成登录状态
	logRequest = requests.Request('GET', url_login,cookies=res0_cookies,headers=headers).prepare()
	#print u"目前的Cookie是："+str(res0_cookies)
	print u"初始化请求,稍等...\n\n"
	s.send(logRequest)

	#Get请求获取数据页面
	resRequest = requests.Request('GET', url_result,cookies=res0_cookies,headers=headers).prepare()	
	res2 = s.send(resRequest)
	print u"获取实时数据成功\n"
	soup = BeautifulSoup(res2.content,"html.parser")
	resNum = soup.find_all("td")
	#序号 申请单号 轮候人 申请日期 公寓名称 房型 优惠价格区间(元/月) 企业审核 申请状态 接受调剂 排名 来源 操作
	resArr = ["序号","申请单号","轮候人","申请日期","公寓名称","房型","优惠价格区间(元/月)","","企业审核","申请状态","接受调剂","排名","来源"]	
	# print soup.html
	# print len(resNum)
	# for i in range(12):
	# 	if i==7:
	# 		continue
	# 	print resArr[i]+":"+resNum[i].text.strip().replace(" ","")
	print u"目前排名为："+resNum[11].text.strip().replace(" ","")
	return int(resNum[11].text.strip().replace(" ",""))

if __name__ == "__main__":
	main()