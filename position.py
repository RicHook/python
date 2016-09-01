#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# 2016-8-26 First edition 
# @Author RichHook

import sys
import time
import urllib2
import os
import difflib
import smtplib
from time import strftime,localtime
from email.MIMEText import MIMEText
from email.Header import Header

mailto_list=['yangyunwei@1006.tv'] 
mail_host="smtp.126.com"  	#设置服务器
mail_user="python_112"    	#用户名
mail_pass="ft4703895"     	#口令 
mail_postfix="126.com"    	#发件箱的后缀
more_num = ['146671', '2288776', '2116009', '1964120']
determine = 0



def send_mail(to_list,sub,content) :
        me = "SSDB-48" + "<" + mail_user + "@" + mail_postfix + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf_8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = to_list
        try :
                server = smtplib.SMTP()
                server.connect(mail_host)
                server.login(mail_user,mail_pass)
                server.sendmail(me, to_list, msg.as_string())
                server.close()
                return True
        except Exception, e :
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
	if '+' in diff or '-' in diff :
		os.remove('/tmp/file/' + num + '.txt')
		os.rename('/tmp/file/temp' + num + '.txt', '/tmp/file/' + num + '.txt')
	else :
		os.remove('/tmp/file/temp' + num + '.txt')
	
	
def thelast() :
	global determine
	alx = int(os.popen("egrep  '\-|\+' /tmp/change |wc -l").read())
	if alx % 2 == 0 :
		code_list = (os.popen("grep  '-' /tmp/change  |awk '{print $2}'").read()).split('\n')
		code_list.remove('')
		for code in code_list :
			cmd = "grep %s /tmp/change |awk '{print $3}'" % (code)
			number_list = (os.popen(cmd).read()).split('%\n')
			number_list.remove('')
			if len(number_list) == 1 :
				determine += 1
			else :
				difference = abs(int(number_list[0]) - int(number_list[1]))
				if difference > 5 :
					determine += 1
	else :
		determine += 1
	print determine	


if __name__ == "__main__" :
	print '%s :time' %strftime('%Y-%m-%d %H:%M:%S',localtime())
	if os.path.exists('/tmp/change') :
		os.remove('/tmp/change')
	else :
		changefile = open('/tmp/change', 'w')
		changefile.close()
	for num in more_num :
		fla = flag(num)
		print fla
		if fla == 0 :
			emptyfile = open('/tmp/file/temp' + num + '.txt', 'w')
        		emptyfile.close()
			diffile(num)
			continue
		if os.path.exists('/tmp/file/' + num + '.txt') :
			Dictionaries = catch(num)
			tempfile(num, Dictionaries)
			diffile(num)
		else :
			Dictionaries = catch(num)
			writefile(num, Dictionaries)
	else :
		thelast()
		if determine != 0 :
			file = open("/tmp/change")
	                line = file.read()
        	        file.close()
			for mailto in mailto_list :
              			if send_mail(mailto, "Change of position", line):
                       			print "Send success"
                		else:
					print "Send fail"

