#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
LEAF_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sys
sys.path.insert(0, LEAF_PATH)

from leaf.models.user_model import User
from leaf.models.note import Note

from leaf.extentions import db

def add_users():
    print 'add users......'
    User.create('liaofeng', '123456', 'liaofeng.pro@gmail.com')
    User.create('huangxin', '111111', 'huangxinms@gmail.com')

def add_notes():
    print 'add notes......'
    liaofeng = User.query_obj.get_by_email('liaofeng.pro@gmail.com')
    huangxin = User.query_obj.get_by_email('huangxinms@gmail.com')
    for user in [liaofeng, huangxin]:
        content = '''
            寻寻觅觅，
            冷冷清清，
            凄凄惨惨戚戚。
            乍暖还寒时候，
            最难将息。
            三杯两盏淡酒，
            怎敌他、晚来风急？
            雁过也，
            正伤心，
            却是旧时相识。

            满地黄花堆积。
            憔悴损，
            如今有谁堪摘？
            守著窗儿，
            独自怎生得黑？
            梧桐更兼细雨，
            到黄昏、点点滴滴。
            这次第，
            怎一个、愁字了得！'''
        Note.create(user.id, content)

        content = '''
            常记溪亭日暮，
            沉醉不知归路。
            兴尽晚回舟，
            误入藕花深处。
            争渡，争渡，
            惊起一滩鸥鹭。 '''
        Note.create(user.id, content)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    add_users()
    add_notes()
