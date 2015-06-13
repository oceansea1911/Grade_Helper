#-*- coding:UTF-8 -*-
import urllib,urllib2,cookielib
import os
from PIL import Image,ImageEnhance,ImageFilter 
from pytesser import *
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

#==========第一次get请求，获得验证码图片的下载地址========
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
username=r'2014110824'
req=urllib2.Request(url=r'http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx',headers=header)
resp=urllib2.urlopen(req)
result=resp.read()

id=result.find(r'id="contentParent_ValidateCode')
src=result.find(r'src=',id)
align=result.find(r'align=',src)
html=result.find(r'<html')
form=result.find(r'<form',html)
path=result[src+8:align-2]
path=r'http://yjxt.bupt.edu.cn/'+path
print path

#============第二次get请求下载验证码图片============
req_image=urllib2.Request(url=path,headers=header)
resp_image=urllib2.urlopen(req_image)
print '=====111==='

result_image=resp_image.read()
open(r'e:\ValidateImage.png','wb').write(result_image)
#============将验证码图片转换为文本=================
os.chdir('c:\Python27\Lib\site-packages\pytesser')
image=Image.open(r'f:\ValidateImage.png')
if len(image.split())==4:
	r,g,b,a=image.split()
	image=Image.merge('RGB',(r,g,b))
	image.save(r'e:\ValidateImage.bmp')
else:
	image.save(r'd:\ValidateImage.bmp')
image1=Image.open(r'e:\ValidateImage.bmp')
code=image_to_string(image1)
print code

#=================post模拟登陆
postdata={r'__EVENTTARGET':r'ctl00$contentParent$btLogin',r'ctl00$contentParent$btLogin':'',r'__VIEWSTATE':r'/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MTMxOTEzNTkwOGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U=',
			r'__EVENTVALIDATION':r'/wEdAAaRoJvWBQsM4Q26lLyNH316cybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=',r'ctl00$contentParent$UserName':'2014110824',r'ctl00$contentParent$PassWord':'buptbupt1',r'ctl00$contentParent$ValidateCode':code}

postdata=urllib.urlencode(postdata)
#req1=urllib2.Request(url='http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=%2fgstudent%2floging.aspx',data=postdata,headers=header)
req1=urllib2.Request(url='http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=%2fgstudent%2floging.aspx%3fundefined',data=postdata,headers=header)

resp1=urllib2.urlopen(req1)
result1=resp1.read()
if '通知公告' in result1:
	print 'success to login'
open(r'f:\login.txt','w').write(result1)

#==============获取课程列表
req2=urllib2.Request(url=r'http://yjxt.bupt.edu.cn/Gstudent/Course/StudentScoreQuery.aspx?EID=l0RCAjrC!60Alnrcjky12Ad6vU4OJDrqYylAGKDjRFO3OCFxhesOvg==&UID='+username,headers=header)
resp2=urllib2.urlopen(req2)
result2=resp2.read()
open(r'f:\list.txt','w').write(result2)

table_s=result2.find(r'<table')
table_e=result2.find(r'</table',table_s)
table=result2[table_s:table_e]

reg=r'<td.*?>(.*?)</td>'
pattern=re.compile(reg)
thlist=re.findall(pattern,table)
grade='hello: \n'
i=0
row=1
for st in thlist:
	if i%11==0:
		grade+='\n'
		row+=1
	if i%11==1:
		grade+=st+':'
	if i%11==6:
		grade+=st
	i+=1
print grade.decode('utf-8').encode('gb2312')

raw_input()

