#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sys
import message
reload(sys)
from django.http import HttpResponse, HttpResponseRedirect
sys.setdefaultencoding('utf-8')

class WechatResponse(object):
    def __init__(self, wechat_id, corp_id, timestamp, nonce):
        self.wechat_id = wechat_id
        self.corp_id = corp_id
        self.timestamp = timestamp
        self.nonce = nonce

    def response(self, **kwargs):
        return HttpResponse("")

class EntryResponse(WechatResponse):
    def __init__(self, wechat_id, corp_id, timestamp, nonce):
        super(EntryResponse, self).__init__(wechat_id, corp_id, timestamp, nonce)
    def response(self, articles):
        news_message = message.NewsMessage(self.wechat_id,
                                           self.corp_id,
                                           self.timestamp,
                                           articles)
        ret, msg = news_message.encrypt(self.nonce)
        return HttpResponse(msg)
