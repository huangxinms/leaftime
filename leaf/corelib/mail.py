# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

from leaf.config import *


def send_regist_mail(mail_to):
    try:
        title = '欢迎注册Heytime'
        body = '请点击完成注册'
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

