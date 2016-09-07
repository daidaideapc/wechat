#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from wechat import settings
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

# 检测是否有这个用户，如果没有就新建
def check_user(wechat_id):
    api = common.admin_api
    if User.objects.filter(wechat_id=wechat_id):
        return User.objects.get(wechat_id=wechat_id)
    # 没找到用户就新建一个
    user_info = api.get_user_info(wechat_id)
    if user_info == None:
        return None
    new_user = User(wechat_id=wechat_id)
    if "name" in user_info:
        new_user.name = user_info["name"]
    if "mobile" in user_info:
        new_user.mobile = user_info["mobile"]
    if "gender" in user_info:
        new_user.gender = user_info["gender"]
    if "email" in user_info:
        new_user.email = user_info["email"]
    new_user.save()
    return new_user

def delete_user(wechat_id):
    api = common.admin_api
    if User.objects.filter(wechat_id=wechat_id):
        User.objects.get(wechat_id=wechat_id).delete()
        return True
    else:
        return False

def change_order(user, order_type, eat, order_date=None):
    if order_date == None:
        order_date = datetime.date.today()
        # TODO 订午餐, 周一到周四是定第二天的午饭
        if order_type == "lunch":
            if order_date.isoweekday() in [1, 2, 3, 4]:
                order_date += datetime.timedelta(days=1)
            # 星期日超过中午11点的话，就订下周一的午餐
            elif order_date.isoweekday() == 7:
                if datetime.datetime.today().hour >= 11:
                    order_date += datetime.timedelta(days=1)
    if Order.objects.filter(user=user, date=order_date, order_type=order_type):
        order = Order.objects.get(user=user, date=order_date, order_type=order_type)
        order.eat = eat
        order.order_type = order_type
        order.category = user.order_category
        order.save()
        return order
    else:
        order = Order(user=user, order_type=order_type, date=order_date, eat=eat)
        order.save()
        return order

# 如果没有订单，就按照这个用户的默认设置来下单
def check_order(user, order_type):
    # TODO 订午餐, 周日到周四是定第二天的午饭
    order_date = datetime.date.today()
    if order_type == "lunch":
        if order_date.isoweekday() in [1, 2, 3, 4]:
            order_date += datetime.timedelta(days=1)
        # 星期日超过中午11点的话，就订下周一的午餐
        elif order_date.isoweekday() == 7:
            if datetime.datetime.today().hour >= 11:
                order_date += datetime.timedelta(days=1)
    if Order.objects.filter(user=user, date=order_date, order_type=order_type):
        return Order.objects.get(user=user, date=order_date, order_type=order_type)
    else:
        order = Order(user=user, order_type=order_type, date=order_date, eat=user.default_order, category=user.order_category)
        order.save()
        return order

def get_order_msg(user_list, order_type):
    api = common.admin_api
    for u in user_list:
        u = check_user(u["userid"])
        # 默认订餐的人才自动生成订单
        if u.default_order:
            check_order(u, order_type)

    order_date = datetime.date.today()
    if order_type == "lunch":
        if order_date.isoweekday() in [1, 2, 3, 4]:
            order_date += datetime.timedelta(days=1)
        # 星期日超过中午12点的话，就订下周一的午餐
        elif order_date.isoweekday() == 7:
            if datetime.datetime.today().hour >= 12:
                order_date += datetime.timedelta(days=1)
    order_list = Order.objects.filter(date=order_date, order_type=order_type, eat=True)
    msg = []
    type_map = {}
    type_map["lunch"] = "午餐"
    type_map["dinner"] = "晚餐"
    msg.append(str(order_date) + " " + type_map[order_type] + ":" + str(len(order_list)) + "人")
    if order_type == "dinner":
        # 肉
        order_list = Order.objects.filter(date=order_date, order_type=order_type, eat=True, category="meat")
        msg.append(str(order_date) + " " + type_map[order_type] + " 肉:" + str(len(order_list)) + "人")
        for o in order_list:
            msg.append(o.user.name + " 肉")
        order_list = Order.objects.filter(date=order_date, order_type=order_type, eat=True, category="vegetable")
        msg.append(str(order_date) + " " + type_map[order_type] + " 素:" + str(len(order_list)) + "人")
        for o in order_list:
            msg.append(o.user.name + " 素")
    else:
        for o in order_list:
            msg.append(o.user.name)
    return msg

def order_setting_get(request, wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没权限","context": "你不是我们的人！" }
        return param
    param = {"wechat_id": wechat_id, "auto_order": user.default_order,"default_category": user.order_category}
    return param

def order_setting_post(request, wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没权限","context": "你不是我们的人！" }
        return param
    auto_order = (request.POST['auto_order'] == 'True')
    default_category = request.POST['default_category']
    user.default_order = auto_order
    user.order_category = default_category
    user.save()
    param = { "title": "订餐设置","context": "修改成功"}
    return param

def order_form_get(request, wechat_id):
    order_date = datetime.date.today()
    dinner_order_date = common.date_to_string(order_date)
    if order_date.isoweekday() in [1, 2, 3, 4]:
        order_date += datetime.timedelta(days=1)
    # 星期日超过中午11点的话，就订下周一的午餐
    elif order_date.isoweekday() == 7:
        if datetime.datetime.today().hour >= 11:
            order_date += datetime.timedelta(days=1)
    lunch_order_date = common.date_to_string(order_date)
    param = { "wechat_id": wechat_id,"lunch_order_date": lunch_order_date,"dinner_order_date": dinner_order_date}
    return param

def order_form_post(request, wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没权限","context": "你不是我们的人！" }
        return param
    lunch_order_date = common.string_to_date(request.POST['lunch_order_date'])
    dinner_order_date = common.string_to_date(request.POST['dinner_order_date'])
    change_order(user, "lunch", request.POST['lunch_radios'] == "eat", order_date=lunch_order_date)
    dinner = change_order(user, "dinner", request.POST['dinner_radios'] != "not_eat", order_date=dinner_order_date)
    dinner.category = request.POST['dinner_radios']
    dinner.save()
    param = {"title": "订餐","context": "订餐成功"}
    return param

def order_suggest_get(request, wechat_id):
    param = {"wechat_id":wechat_id}
    return param

def order_suggest_post(request,wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没有权限","context": "你是怎么进来的！！！" }
        return param
    suggest = Suggest()
    suggest.user = user
    suggest.date = datetime.date.today()
    suggest.title = request.POST['suggest_title']
    suggest.suggest_text = request.POST['suggest_text']
    suggest.save()
    param = {"title":"吐槽达人","context":"每天吐槽，健康饮食"}
    return param

def order_view(request, wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没权限","context": "你不是我们的人！" }
        return param
    if user.role_list == None:
        user.role_list = ""
    role_set = set(user.role_list.strip().split(','))
    order_date = datetime.date.today()
    dinner_order_date = order_date
    if order_date.isoweekday() in [1, 2, 3, 4]:
        order_date += datetime.timedelta(days=1)
    # 星期日超过中午11点的话，就订下周一的午餐
    elif order_date.isoweekday() == 7:
        if datetime.datetime.today().hour >= 11:
            order_date += datetime.timedelta(days=1)
    lunch_order_date = order_date
    dinner_order_list = Order.objects.filter(user=user, order_type="dinner", eat=True)[:30]
    lunch_order_list = Order.objects.filter(user=user, order_type="lunch", eat=True)[:30]
    is_order_admin = False
    if 'order_admin' in role_set:
        dinner_order_list = Order.objects.filter(date=dinner_order_date, order_type="dinner", eat=True)
        lunch_order_list = Order.objects.filter(date=lunch_order_date, order_type="lunch", eat=True)
        is_order_admin = True

    args = {}
    args["dinner_order_list"] = dinner_order_list
    args["lunch_order_list"] = lunch_order_list
    args["is_order_admin"] = is_order_admin
    args["dinner_order_date"] = dinner_order_date
    args["lunch_order_date"] = lunch_order_date
    return args

def suggest_view(request, wechat_id):
    user = check_user(wechat_id)
    if user == None:
        param = { "title": "你没权限","context": "你不是我们的人！" }
        return param
    if user.role_list == None:
        user.role_list = ""
    role_set = set(user.role_list.strip().split(','))
    suggest_list = Suggest.objects.filter(user=user)
    is_order_admin = False

    args = {}
    args["suggest_list"] = suggest_list
    args["is_order_admin"] = is_order_admin


    if 'order_admin' in role_set:
        is_order_admin = True
        suggest_list = Order.objects.filter()
        suggest_num = len(suggest_list)
        args["suggest_list"] = suggest_list
        args["is_order_admin"] = is_order_admin
    return args
