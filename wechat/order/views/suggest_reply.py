#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from wechat import settings
from util import wechat_api
from util import common
from order import order_api
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

def suggest_reply(request, wechat_id, suggest_id):
    if request.method == 'GET':
        return render(request,'order/suggest_reply.html', order_api.suggest_reply_get(request,wechat_id, suggest_id))
    elif request.method == 'POST':
        return render(request,'order/submitted_info.html', order_api.suggest_reply_post(request,suggest_id))
