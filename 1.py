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
reload(sys)
sys.setdefaultencoding('utf8') 

class Student_Grade(object):
	"""docstring for student_grade"""
	islogin=False
	def __init__(self):
		print 'ÏµÍ³ÕýÔÚ³õÊ¼»¯...'.encode('gbk')
		self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
		cookie=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		urllib2.install_opener(opener)



#==========µÚÒ»´ÎgetÇëÇó£¬»ñµÃÑéÖ¤ÂëÍ¼Æ¬µÄÏÂÔØµØÖ·========
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

	#============µÚ¶þ´ÎgetÇëÇóÏÂÔØÑéÖ¤ÂëÍ¼Æ¬============
	def get_image(self,path):
		req_image=urllib2.Request(url=path,headers=self.header)
		resp_image=urllib2.urlopen(req_image)
		result_image=resp_image.read()
		open(r'f:\ValidateImage.png','wb').write(result_image)
	#============½«ÑéÖ¤ÂëÍ¼Æ¬×ª»»ÎªÎÄ±¾=================
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
		print 'ÕýÔÚ³¢ÊÔÓë·þÎñÆ÷È¡µÃÁ´½Ó£¬ÇëÉÔºó...'.encode('gbk')
		return code

	#=================postÄ£ÄâµÇÂ½
	def login(self,username,passWord,code):
		postdata={r'__EVENTTARGET':r'ctl00$contentParent$btLogin',r'ctl00$contentParent$btLogin':'',r'__VIEWSTATE':r'/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MTMxOTEzNTkwOGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U=',
				r'__EVENTVALIDATION':r'/wEdAAaRoJvWBQsM4Q26lLyNH316cybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=',r'ctl00$contentParent$UserName':username,r'ctl00$contentParent$PassWord':passWord,r'ctl00$contentParent$ValidateCode':code}
		postdata=urllib.urlencode(postdata)
		req=urllib2.Request(url='http://yjxt.bupt.edu.cn/gstudent/ReLogin.aspx?ReturnUrl=%2fgstudent%2floging.aspx%3fundefined',data=postdata,headers=self.header)
		resp=urllib2.urlopen(req)
		result=resp.read()
		print 'ÕýÔÚµÇÂ½'.encode('gbk')
		if 'Í¨Öª¹«¸æ' in result:
			islogin=True
		return islogin
		
			
	#	open(r'f:\login.txt','w').write(result)

	#==============»ñÈ¡¿Î³ÌÁÐ±í
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



def send_email(msg):
	from_addr=r'h1224048104@163.com'
	password=r'plao01!'
	smtp_server=r'smtp.163.com'
#	to_addr='mypython_server@163.com'
#	to_addr=r'1224048104@qq.com'
	to_addr=r'h1224048104@163.com'
	server=smtplib.SMTP(smtp_server,25)
#	server.set_debuglevel(1)
	server.login(from_addr,password)
	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()


					

print '==================³É¼¨²éÑ¯ÖúÊÖGrade_Helper_V2.0==============='.encode('gbk')
print 'Auther:  ÍôÅìÑó'.encode('gbk')
print '\n\n'

while True:
	str1='ÇëÊäÈëÓÃ»§Ãû£º'
	str2='ÇëÊäÈëÃÜÂë£º'
	username=raw_input(str1.encode('gbk'))
	passWord=raw_input(str2.encode('gbk'))
	mygrade=Student_Grade()
	mygrade.get_image(mygrade.get_image_url())

	
	if mygrade.login(username,passWord,mygrade.image2text()):
		print 'µÇÂ½³É¹¦£¬ÕýÔÚ»ñÈ¡¿Î³ÌÁÐ±í...'.encode('gbk')
		break
	else:
		print 'ÓÃ»§Ãû»òÃÜÂë´íÎó£¬ÇëÖØÐÂÊäÈë'.encode('gbk')

row,grade=mygrade.get_grade(username)

print '²éÑ¯³É¼¨ÈçÏÂ£º'.encode('gbk')
print grade.decode('utf-8').encode('gb2312')
print '¹²'.encode('gbk')+str(row)+'ÃÅ¹¦¿Î³É¼¨'.encode('gbk')


msg = MIMEText(grade,'plain','utf-8')
msg['Subject']=Header(u'成绩查询结果','utf-8').encode()
send_email(msg)
print '³É¼¨ÒÔ·¢ËÍµ½ÓÊÏä£¬Çë¼°Ê±²é¿´'.encode('gbk')
print '=================================================================='
raw_input()