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
    content = f.read()
    content = content.split('\n')
    order_date = datetime.date.today()
    order_date = order_date.isoweekday()
    order_list = content[order_date - 1]
    order_list = order_list.split()
    contest = "辣餐为：" + order_list[0] + "\n不辣为：" + order_list[1] + "\n素餐为：" + order_list[2] + "\n\n"
    return contest
    
#def get_order():
#    user = order_api.check_user("an839274949")
#    #order_lunch_result = order_api.check_order(user,"lunch")
#    #order_dinner_result = order_api.check_order(user,"dinner")
#    #print order_lunch_result,order_dinner_result
#    print user.order_category
#    user.order_category = "not_spicy"
#    user.save()
#    print user.order_category

def remind(exclude={}):
    content = read_order()
    #print content
    #get_order()
    user_list = common.admin_api.get_user_list()["userlist"]
    for user in user_list:
        # 如果在去除列表中则不推送
        if user["userid"] in exclude:
            continue
        user = order_api.check_user(user["userid"])
        order_api.check_order(user, "lunch")
        #order_api.check_order(user, "dinner")
	wechat_id = user.wechat_id
	title = '今日晚餐菜单：'
	#if user.default_order != True:
	#    user_type = "您未预定晚餐"
	#elif user.order_category == "not_spicy":
	#    user_type = "已为您预定：不辣"
	#elif user.order_category == "spicy":
	#    user_type = "已为您预定：辣餐"
	#else :
	#    user_type = "已为您预定：素餐"
	#context_next = "\n\n修改本次订单请于下午五点前点击修改订单，选择相应餐品，点击提交！修改提交后，可点击查看订单验证是否修改成功。\n如需修改默认自动订餐方式，请点击自动订餐，修改保存！\n杜绝浪费，如不订餐请及时取消！"
	context_next = "\n\n晚餐下单截止时间：下午5点。\n\n自动订餐功能已下线。请需要预定晚餐的同事点击‘今日晚餐’选择相应餐品种类，点击提交！\n晚餐请按餐品种类拿取自己的晚餐，请勿错拿！多谢合作！"
	context = content + context_next
	#wechat_id = "an839274949"
	wechat_id = str(wechat_id)
	#print user.name,wechat_id,str(title),str(context)
    	common.admin_api.send_test_message([wechat_id], str(title),str(context))

if __name__:
    exclude = {}
    exclude["mud000"] = True
    remind(exclude)
