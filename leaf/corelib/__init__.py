# -*- coding: utf-8 -*-
import datetime
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def format_textarea(content):
    return content.replace(' ','&nbsp;').replace('\r','<br/>')

def get_local_date(dt):
    return dt.strftime('%Y年%m月%d日').decode('utf-8')

def get_local_weekday(dt):
    dic = {0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'日'}
    return u'星期%s' %dic[dt.weekday()].decode('utf-8')


class cache:

    def __init__(self,name_format,expire=0):
        self.name_format = name_format
        self.expire = expire

    def __call__(self,f):
        def wrapped(*args, **kwargs):
            args_values, _ = self.__get_args(f, args, kwargs)
            entry_name = self.name_format.format(**args_values)
            value = mc.get(entry_name)

            if value is None:
                value = f(*args, **kwargs)
                mc.set(entry_name, value, self.expire)
            return value
        return wrapped

    def __get_args(self, f, args, kwargs):
        import inspect
        args_names, _, _, defaults = inspect.getargspec(f)
        passed_args = {}
        if defaults is not None:
            passed_args = dict(zip(args_names[-len(defaults):], defaults))
        passed_args.update(dict(zip(args_names, args)))
        passed_args.update(kwargs)
        passed_varargs = args[len(args_names):]
        return passed_args, passed_varargs
