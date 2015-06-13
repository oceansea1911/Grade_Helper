#-*- coding:UTF-8 -*-
import urllib,urllib2,cookielib
import os
from PIL import Image,ImageEnhance,ImageFilter 
from pytesser import *
import re
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.header import Header
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8') 

class Student_Grade(object):
	"""docstring for student_grade"""
#	isLogin=False
	def __init__(self):
		self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
		cookie=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		urllib2.install_opener(opener)



#==========第一次get请求，获得验证码图片的下载地址========
	def get_image_url(self):
		req=urllib2.Request(url=r'http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx',headers=self.header)
		resp=urllib2.urlopen(req)
		result=resp.read()
		reg=r'(/Public/ValidateCode.aspx\?image=[0-9]{7,10})'
		pattern=re.compile(reg)
		path=re.findall(pattern,result)
	#	id=result.find(r'id="contentParent_ValidateCode')
	#	src=result.find(r'src=',id)
	#	align=result.find(r'align=',src)
	#	html=result.find(r'<html')
	#	form=result.find(r'<form',html)
	#	path=result[src+8:align-2]
		path=r'http://yjxt.bupt.edu.cn/'+path[0]
		return path

	#============第二次get请求下载验证码图片============
	def get_image(self,path):
		req_image=urllib2.Request(url=path,headers=self.header)
		resp_image=urllib2.urlopen(req_image)
		result_image=resp_image.read()
		open(r'f:\ValidateImage.png','wb').write(result_image)
	#============将验证码图片转换为文本=================
	def image2text(self):
		os.chdir('C:\Python27\Lib\site-packages\pytesser')
		image=Image.open(r'f:\ValidateImage.png')
		if len(image.split())==4:
			r,g,b,a=image.split()
			image=Image.merge('RGB',(r,g,b))
			image.save(r'F:\ValidateImage.bmp')
		else:
			image.save(r'F:\ValidateImage.bmp')
		image1=Image.open(r'F:\ValidateImage.bmp')
		code=image_to_string(image1)
		return code

	#=================post模拟登陆
	def login(self,username,passWord,code):
		isLogin=False
		postdata={r'__EVENTTARGET':r'ctl00$contentParent$btLogin',r'ctl00$contentParent$btLogin':'',r'__VIEWSTATE':r'/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MTMxOTEzNTkwOGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U=',
				r'__EVENTVALIDATION':r'/wEdAAaRoJvWBQsM4Q26lLyNH316cybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=',r'ctl00$contentParent$UserName':username,r'ctl00$contentParent$PassWord':passWord,r'ctl00$contentParent$ValidateCode':code}
		postdata=urllib.urlencode(postdata)

		req=urllib2.Request(url='http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=%2fgstudent%2floging.aspx%3fundefined',data=postdata,headers=self.header)
		resp=urllib2.urlopen(req)
		result=resp.read()
		if '通知公告' in result:
			isLogin=True
		return isLogin
		
	#	open(r'f:\login.txt','w').write(result)

	#==============获取课程列表
	def get_grade(self,username):
		req=urllib2.Request(url=r'http://yjxt.bupt.edu.cn/Gstudent/Course/StudentScoreQuery.aspx?EID=l0RCAjrC!60Alnrcjky12Ad6vU4OJDrqYylAGKDjRFO3OCFxhesOvg==&UID='+username,headers=self.header)
		resp=urllib2.urlopen(req)
		result=resp.read()
		table_s=result.find(r'<table')
		table_e=result.find(r'</table',table_s)
		table=result[table_s:table_e]

		reg=r'<td.*?>(.*?)</td>'
		pattern=re.compile(reg)
		thlist=re.findall(pattern,table)
		grade=''
		i=0
		row=0
		for st in thlist:
			if i%11==0:
				grade+='\n'
				row+=1
			if i%11==1:
				grade+=st+':'
			if i%11==6:
				grade+=st
			i+=1
		return row,grade

def send_email(grade,args):
	msg = MIMEText(grade,'plain','utf-8')
	msg['Subject']=Header(u'成绩查询结果','utf-8').encode()

	from_addr=r'h1224048104@163.com'
	password=r'buptPLAO01!'
	smtp_server=r'smtp.163.com'
#	to_addr='mypython_server@163.com'
#	to_addr=r'1224048104@qq.com'
#	to_addr=r'h1224048104@163.com'
	to_addr=args
#	to_addr=r'597241336@qq.com'
	server=smtplib.SMTP(smtp_server,25)
#	server.set_debuglevel(1)
	server.login(from_addr,password)
	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()	

print '==================成绩查询助手Grade_Helper_V2.0==============='.encode('gbk')
print 'Auther:  汪澎洋'.encode('gbk')
print '\n'

while True:
	str1='请输入用户名：'
	str2='请输入密码：'
	username=raw_input(str1.encode('gbk'))
	passWord=raw_input(str2.encode('gbk'))
	addr=raw_input('请输入成绩查收邮箱(非必填)：'.encode('gbk'))
	mygrade=Student_Grade()
	mygrade.get_image(mygrade.get_image_url())

	
	if mygrade.login(username,passWord,mygrade.image2text()):
		print '登陆成功'.encode('gbk')
		break
	else:
		print '用户名或密码错误'.encode('gbk')

row1,grade1=mygrade.get_grade(username)

print '正在获取成绩列表'.encode('gbk')
print grade1.decode('utf-8').encode('gb2312')
print '共查询到'.encode('gbk')+str(row1)+'门功课成绩'.encode('gbk')
print '查询日期：'.encode('gbk'),time.asctime()

grade1+='\n\n'+'查询日期：'+time.asctime()


#msg = MIMEText(grade1,'plain','utf-8')
#msg['Subject']=Header(u'成绩查询结果','utf-8').encode()
if addr=='':
	pass
else:
	send_email(grade1,addr)
	print '【已将成绩发送到邮箱，请注意查收】'.encode('gbk')
	print '=================================================================='

while True:
	i=0
	while i<1000000:
		i+=1
	row2,grade2=mygrade.get_grade(username)
	if row2==row1:
		print '---------------成绩没有更新---------------'.decode('utf-8').encode('gb2312')
	else:
		grade=grade2[len(grade1):]
		print '-----新增成绩-----'
		print grade
		print '更新日期：'.decode('utf-8').encode('gb2312')+time.asctime()
		if addr=='':
			pass
		else:
			send_email(grade1,addr)
			print '【已将成绩发送到邮箱，请注意查收】'.encode('gbk')
			print '=================================================================='


raw_input()