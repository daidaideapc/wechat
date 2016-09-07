#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from wechat import settings
from order.models import User
from order.models import Order
from order import order_api
from util import message
from util import wechat_api
from util import common
from util import wechat_response
from util import parse_event
from util import event_controller
from util.WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.
def index(request):
    msg_signature = request.GET["msg_signature"]
    timestamp = request.GET["timestamp"]
    nonce = request.GET["nonce"]
    data = request.body
    #sEchoStr = request.GET["echostr"]
    #ret,sMsg=common.wxcpt.VerifyURL(msg_signature, timestamp, nonce, sEchoStr)
    #return HttpResponse(sMsg)
    ret,sMsg=common.wxcpt.DecryptMsg(data, msg_signature, timestamp, nonce)
    xml_tree = ET.fromstring(sMsg)
    wechat_id = xml_tree.find("FromUserName").text
    event = parse_event.parse_event(xml_tree)
    if event:
        controller = event_controller.EventController(event)
        return controller.get_response(wechat_id, settings.corp_id, timestamp, nonce)
    text_message = message.TextMessage(wechat_id, settings.corp_id, timestamp, wechat_id + "搞不懂你要干什么", '3')
    ret,sEncryptMsg=common.wxcpt.EncryptMsg(text_message.get_xml(), nonce, timestamp)
    return HttpResponse(sEncryptMsg)

def entry(request):
    return render(request, 'order/entry.html', {})

