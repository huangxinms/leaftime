#-*- coding:utf-8 -*-
import os
import json
import re
import random

from leaf.config import TEMPLATES_FILE_PATH, STATIC_FILE_PATH

class NS:

    @classmethod
    def set_static_versions(cls):
        versions = cls.get_file_versions()
        files = cls.get_all_template_files()
        for file_path in files:
            content,links = cls.get_all_static_links(file_path)
            for link in links:
                # 如果找不到版本号则产生10位的随机字符串
                version = versions.get(link, ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()',10)))
                content = content.replace(link, '%s?v=%s'%(link, version))
            f = open(file_path, 'w')
            f.write(content)

    @classmethod
    def get_file_versions(cls):
        files = cls.get_all_static_files()
        result = {}
        for k in files:
            v = cls.get_version_from_git(k)
            ob_path = k.replace(STATIC_FILE_PATH,'')
            result[ob_path] = v
        return result

    @classmethod
    def get_all_static_files(cls):
        result = []
        for dirpath,dirnames,filenames in os.walk(STATIC_FILE_PATH):
            for filename in filenames:
                result.append(dirpath + '/' + filename)
        return result

    @classmethod
    def get_version_from_git(cls, file_name):
        rd = os.popen("cd %s && git log %s | sed -n 1p | awk -F ' ' '{print $2}'" %(STATIC_FILE_PATH,file_name))
        ver = rd.read()
        rd.close()
        ver = ver.strip()
        return ver

    @classmethod
    def get_all_template_files(cls):
        result = []
        for dirpath,dirnames,filenames in os.walk(TEMPLATES_FILE_PATH):
            for filename in filenames:
                result.append(dirpath + '/' + filename)
        return result

    @classmethod
    def get_all_static_links(cls, file_path):
        f = open(file_path, 'r')
        content = f.read()
        f.close()
        static_links = re.findall('{{\s+static\s+}}\/(\S+)[\"\']', content)
        return content,static_links

if __name__ == '__main__':
    NS.set_static_versions()
