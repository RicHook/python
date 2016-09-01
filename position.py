#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author RichHook

import sys
import time
import urllib2
import os
import difflib
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header

mailto_list=['yangyunwei@1006.tv',] 
mail_host="smtp.163.com"  #设置服务器
mail_user="python_112"    #用户名
mail_pass="www.1006.tv"   #口令 
mail_postfix="163.com"  #发件箱的后缀
more_num = ['146671', '2288776', '2116009', '718335']
determine = 0

def send_mail(to_list,sub,content):
        me = "SSDB-48" + "<" + mail_user + "@" + mail_postfix + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf_8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
                server = smtplib.SMTP()
                server.connect(mail_host)
                server.login(mail_user,mail_pass)
                server.sendmail(me, to_list, msg.as_string())
                server.close()
                return True
        except Exception, e     :
            print str(e)
            return False
def flag(num) :
	flag = 0
	html = 'http://moniapi.eastmoney.com/webapi/json.aspx?type=user_hold&zh=' + num + '&recIdx=0&recCnt=100&js=zuheinfo49988359((x))&callback=zuheinfo49988359&_=1471491487857'
        more_list = urllib2.urlopen(html).read().split(",")
	for text in more_list :
		if "holdPos" in text :
			flag += 1
	else :
		return flag	

def catch(num) :
	html = 'http://moniapi.eastmoney.com/webapi/json.aspx?type=user_hold&zh=' + num + '&recIdx=0&recCnt=100&js=zuheinfo49988359((x))&callback=zuheinfo49988359&_=1471491487857'
        more_list = urllib2.urlopen(html).read().split(",")
        holdPos = [early_holdPos for early_holdPos in more_list if "holdPos" in early_holdPos]
        code = [early_code for early_code in more_list if "__code" in early_code]
        Dictionaries = {}
        for i in range(len(holdPos)) :
                Dictionaries[code[i].split(":")[1].replace('"','')] = int(float(holdPos[i].split(":")[1].replace('"','')) * 100)
	return Dictionaries


def writefile(num, Dictionaries) :
        file1 = open('/tmp/file/' + num + '.txt', 'w')
        for key in Dictionaries :
                file1.write('%s    %d%s%s' % (key, Dictionaries[key], '%', os.linesep))
        file1.close()


def tempfile(num, Dictionaries) :
	file2 = open('/tmp/file/temp' + num + '.txt', 'w')
	for key in Dictionaries :
		file2.write('%s    %d%s%s' % (key, Dictionaries[key], '%', os.linesep))
        file2.close()


def diffile(num) :
	global determine
	a = open('/tmp/file/' + num + '.txt', 'U').readlines()
	b = open('/tmp/file/temp' + num + '.txt', 'U').readlines()
	output=sys.stdout
	outputfile = open('/tmp/change', 'a')
	sys.stdout = outputfile
	outputfile.write('%s%s' % (num, os.linesep))
	sys.stdout.writelines(difflib.ndiff(a, b))
	outputfile.write(os.linesep * 4)
	outputfile.close()
	sys.stdout=output
	diff = open('/tmp/change', 'U').read()
	if '?' in diff :
		os.remove('/tmp/file/' + num + '.txt')
		os.rename('/tmp/file/temp' + num + '.txt', '/tmp/file/' + num + '.txt')
		determine += 1
	else :
		os.remove('/tmp/file/temp' + num + '.txt')
		


if __name__ == "__main__" :
	os.remove('/tmp/change')
	for num in more_num :
		fla = flag(num)
		if fla == 0 :
			outputfile = open('/tmp/change', 'a')
        		outputfile.write('%s%s' % (num, os.linesep))
        		outputfile.write(os.linesep * 4)
        		outputfile.close()
			print 'continue'
                	continue
		if os.path.exists(r'/tmp/file/' + num + '.txt') :
			Dictionaries = catch(num)
			tempfile(num, Dictionaries)
			diffile(num, )
		else :
			Dictionaries = catch(num)
			writefile(num, Dictionaries)
	else :
		print determine
		if determine != 0 :
			file = open("/tmp/change")
	                line = file.read()
        	        file.close()
              		if send_mail(mailto_list, "持仓变动", line):
                        	print "发送成功"
                	else:
                                print "发送失败"





















