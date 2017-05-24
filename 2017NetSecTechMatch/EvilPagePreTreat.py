#! python2
# -*-coding: utf-8-*-
# @Time    : 2017/5/13 13:56
# @Author  : Haoranz
# @Function: PreTreat the Data of Evil Page Test in "2017 Network Security Tech Match".
# @InputFormat: 000034,p,3f2e6063f5ecfb1e902e53bb59745197,http://slimmusic.com.ng/mk/login.jsp.htm?tracelog=new_guide_0418_newschp&amp;biz_type=Notifications_Connections&amp;crm_mtn_tracelog_task_id=78a21b92-2ec0-4a74-9c78-04a5f7d45f1b&amp;crm_mtn_tracelog_log_id=13667531608
# @OutputFormat: "No  Result  URL [[Each key&value], [Length of URL, Count of Key&value, [Each len(Key)/len(value)]]]
# @Output: "No:001763	d	URL:http://www.huataijingye.com/newsrg.php	[['7xt5b/gipj1.shtml', '392ap'], [23, 1, [3.4]]]

import UrlValueDecode

def main(filePath, pageType):
    resList = []
    with open(filePath, "r+") as fOpen:
        for iLine in fOpen.readlines():
            iList = iLine.split(',')
            if iList[1] == pageType:
                iResList = []
                iResList.append(strNum(iList[0]))
                iResList.append(iList[1])
                url = iList[3].strip().split('?')
                iResList.append(urlPickup(url[0]))
                if len(url) == 2:
                    iResList.append(UrlValueDecode.paramUrlFormat(url[1]))
                resList.append(iResList)
    for iPrint in resList:
        if len(iPrint) == 4:
            print iPrint[0] + '	' + iPrint[1] + '	' + str(iPrint[2]) + '	' + str(iPrint[3])
        else:
            print iPrint[0] + '	' + iPrint[1] + '	' + str(iPrint[2])


def strNum(strValue):
    return 'No:' + strValue


def urlPickup(strValue):
    try:
        return "URL:" + strValue.split('?')[0]
    except Exception as e:
        return "URL:" + strValue


if __name__ == '__main__':
    # n  Normal Page
    # p  Phishing site
    # d  Fake Website

    # strTest = "a="
    # print requestData(strTest)
    #
    pageType = "d"

    filePath = "..\EvilPageAnalysis\\file_list.txt"
    main(filePath, pageType)
