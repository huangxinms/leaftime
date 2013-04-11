# -*- coding: utf-8 -*-

import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from leaf.config import MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD


def send_regist_mail(mail_to, code):
    def __generate_regist_url():
        f = open('leaf/corelib/regist_mail.tpl','r')
        body = f.read()
        base_url = 'http://42.96.171.102/init?email=%s&code=%s'
        body_url = base_url %(mail_to, code)
        return body.format(body_url)
    try:
        title = '欢迎注册Heytime'
        body = __generate_regist_url()
        __send_mail(mail_to, title, body)
        return True
    except:
        return False

def __send_mail(mail_to,title,text):
    smtp = smtplib.SMTP()
    smtp.connect(MAIL_HOST, MAIL_PORT)
    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)

    msg = MIMEMultipart('alternative')
    msg['From'] = MAIL_USERNAME
    msg['To'] = mail_to
    msg['Subject'] = title
    text = MIMEText(text, 'html')
    msg.attach(text)
    smtp.sendmail(MAIL_USERNAME, mail_to, msg.as_string())
    smtp.quit()

def check_email(email):
    return re.match("(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", email)

