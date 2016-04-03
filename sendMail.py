#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import smtplib 
from email.mime.text import MIMEText

class send_mail:
    def __init__(self,host,user,pwd,postfix):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.postfix = postfix
        
    def send(self,receiver, sub, context): 
##        #构造附件
##        att1 = MIMEText(open('d:\\123.rar', 'rb').read(), 'base64', 'gb2312')
##        att1["Content-Type"] = 'application/octet-stream'
##        att1["Content-Disposition"] = 'attachment; filename="123.doc"'
##        msg.attach(att1)

        sender = self.user + "<"+self.user+"@"+self.postfix+">" 
        msg = MIMEText(context) 
        msg['Subject'] = sub 
        msg['From'] = sender 
        msg['To'] = ";".join(receiver)
        try:
            send_smtp = smtplib.SMTP()
            send_smtp.connect(self.host)
            send_smtp.login(self.user, self.pwd)
            send_smtp.sendmail(sender, receiver, msg.as_string())
            send_smtp.close()
            return True
        except Exception as e :
            return False
