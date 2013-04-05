# -*- coding: utf-8 -*-

import re
import smtplib
from email.mime.text import MIMEText

from leaf.config import *


def send_regist_mail(mail_to, code):
    def __generate_regist_url():
        base_url = 'http://42.96.171.102/init?email=%s&code=%s'
        return base_url %(mail_to,code)
    try:
        title = '欢迎注册Heytime'
        body = __generate_regist_url()
        __send_mail(mail_to,title,body)
        return True
    except:
        return False

def __send_mail(mail_to,title,text):
    smtp = smtplib.SMTP()
    smtp.connect(MAIL_HOST,MAIL_PORT)
    smtp.login(MAIL_USERNAME,MAIL_PASSWORD)

    msg = MIMEText(text)
    msg['From'] = MAIL_USERNAME
    msg['To'] = mail_to
    msg['Subject'] = title
    smtp.sendmail(MAIL_USERNAME,mail_to,msg.as_string())
    smtp.quit()

def check_email(email):
    if re.match("(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", email):
        return True
    return False
