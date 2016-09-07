#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sys
sys.path.append('../../../util')
sys.path.append('../../../')
sys.path.append('../../')
import wechat_api
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wechat.settings")
import django
django.setup()
from order.models import *
from order.views import *
from util import common
from order import order_api
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import time


def read_order():
    f = open('order_list','r')
    order_list = f.read()
    print type(order_list)

def remind(exclude={}):
    read_order()
    return 
    user_list = common.admin_api.get_user_list()["userlist"]
    for user in user_list:
        # 如果在去除列表中则不推送
        if user["userid"] in exclude:
            continue
        user = order_api.check_user(user["userid"])
        order_api.check_order(user, "lunch")
        order_api.check_order(user, "dinner")
        wechat_id = user.wechat_id
        common.admin_api.send_news_message([wechat_id], [{'title': '订餐', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/order_form/' + wechat_id}])

if __name__:
    exclude = {}
    exclude["mud000"] = True
    remind(exclude)
