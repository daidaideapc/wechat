#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from wechat import settings
from util import wechat_api
from util import common
from order.models import *
from order import order_api
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

def view_order(request, wechat_id):
    args = order_api.order_view(request, wechat_id)
    user = order_api.check_user(wechat_id)
    if user == None:
        return render(request,'order/submitted_info.html',args)
    return render(request,'order/view_order.html',args)
