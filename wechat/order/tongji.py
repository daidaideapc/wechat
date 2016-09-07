#!/usr/bin/env python
#-*- encoding:utf-8 -*-
#from wechat import settings
from .models import User
from .models import Order
from .models import Suggest
from util import message
from util import wechat_api
from util import common
from util.WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def tongji():
    user_list = api.get_user_list()["userlist"]
    print len(user_list)
    return 
    dinner_order_list = Order.objects.filter(user=user, order_type="dinner", eat=True).order_by('-date')[:30]
    lunch_order_list = Order.objects.filter(user=user, order_type="lunch", eat=True).order_by('-date')[:30]
    args = {}
    args["is_order_admin"] = False
    if 'order_admin' in role_set:
        dinner_order_list = Order.objects.filter(date=dinner_order_date, order_type="dinner", eat=True)
        lunch_order_list = Order.objects.filter(date=lunch_order_date, order_type="lunch", eat=True)
        args["dinner_spicy_num"] = len(Order.objects.filter(date=dinner_order_date, order_type="dinner", category="spicy", eat=True))
        args["dinner_not_spicy_num"] = len(Order.objects.filter(date=dinner_order_date, order_type="dinner", category="not_spicy", eat=True))
        args["dinner_vegetable_num"] = len(Order.objects.filter(date=dinner_order_date, order_type="dinner", category="vegetable", eat=True))
        args["lunch_order_num"] = len(lunch_order_list)
        args["is_order_admin"] = True

    args["dinner_order_list"] = dinner_order_list
    args["lunch_order_list"] = lunch_order_list
    args["dinner_order_date"] = dinner_order_date
    args["lunch_order_date"] = lunch_order_date
    return args

if __name__ == '__main__':
    tongji()
