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


#def read_order():
#    f = open('order_list','r')
#    content = f.read()
#    content = content.split('\n')
#    order_date = datetime.date.today()
#    order_date = order_date.isoweekday()
#    order_list = content[order_date - 1]
#    order_list = order_list.split()
#    contest = "辣餐为：" + order_list[0] + "\n不辣为：" + order_list[1] + "\n素餐为：" + order_list[2] + "\n\n"
#    return contest
    
#def get_order():
#    user = order_api.check_user("an839274949")
#    #order_lunch_result = order_api.check_order(user,"lunch")
#    #order_dinner_result = order_api.check_order(user,"dinner")
#    #print order_lunch_result,order_dinner_result
#    print user.order_category
#    user.order_category = "not_spicy"
#    user.save()
#    print user.order_category

def remind():
    #content = read_order()
    #print content
    #get_order()
    default_list = ['张丙寅','向枫','王江']
    user_list = common.admin_api.get_user_list()["userlist"]
    for user in user_list:
        # 如果在去除列表中则不推送
        if user["name"] in default_list:
            continue
        user = order_api.check_user(user["userid"])
	order_date = datetime.date.today()
	order_dinner_list = len(Order.objects.filter(date=order_date,user=user,order_type="dinner", eat=True))
	if order_dinner_list == 1:
	    continue
	#wechat_id = user.wechat_id
	context = "您未订餐，距离今日晚餐预定结束还有5分钟，请需要订餐的同事抓紧时间，5点后还有需要预定晚餐的同学及时与管理员联系！如需以后长期取消5分钟提醒推送，请联系管理员！"
	wechat_id = user.wechat_id 
	#wechat_id = "an839274949"
	wechat_id = str(wechat_id)
    	common.admin_api.send_message([wechat_id], str(context))

if __name__:
    remind()
