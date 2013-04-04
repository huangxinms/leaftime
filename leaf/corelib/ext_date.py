# -*- coding: utf-8 -*-

import datetime

def get_local_date(dt):
    return dt.strftime('%Y年%m月%d日').decode('utf-8')

def get_local_weekday(dt):
    dic = {0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'日'}
    return u'星期%s' %dic[dt.weekday()].decode('utf-8')

