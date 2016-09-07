#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import sys
sys.path.append('../')
from order import order_api
reload(sys)
sys.setdefaultencoding('utf-8')
import wechat_response
import message
from django.http import HttpResponse, HttpResponseRedirect

class EventController(object):
    def __init__(self, event):
        self.event = event

    def get_response(self, wechat_id, corp_id, timestamp, nonce):
        event = self.event
        # 关注微信号
        if event == "subscribe":
            order_api.check_user(wechat_id)
            entry_response = wechat_response.EntryResponse(wechat_id, corp_id, timestamp, nonce)
            articles = [{'title':'入职指引', 'picurl': 'http://223.202.85.88/static/image/cloudin.jpg','url': 'http://223.202.85.88/entry'}]
            return entry_response.response(articles)
        # 取关微信号 暂时不做处理
        if event == "unsubscribe":
            return HttpResponse("")
        # 订餐设置
        if event == "order_setting":
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'每日午餐自动订餐设置', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/order_setting/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)
        # 查看订餐情况
        if event == "view_order":
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'查看订单', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/view_order/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)
        ## 订餐反馈
        #if event == "order_suggest":
        #    news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'你就是下一个吐槽达人', 'picurl': 'http://223.202.85.88/static/image/suggest.jpg','url': 'http://223.202.85.88/order_suggest/' + wechat_id}])
        #    ret, msg = news_message.encrypt(nonce)
        #    return HttpResponse(msg)
        # # 查看反馈
        #if event == "suggest_view":
        #    news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'查看吐槽清单', 'picurl': 'http://223.202.85.88/static/image/suggest.jpg','url': 'http://223.202.85.88/suggest_view/' + wechat_id}])
        #    ret, msg = news_message.encrypt(nonce)
        #    return HttpResponse(msg)

        # 订餐表单页面
        #if event == 'order_form':
        #    news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'订餐戳这里', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/order_form/' + wechat_id}])
        #    ret, msg = news_message.encrypt(nonce)
        #    return HttpResponse(msg)
        if event == "spicy":
	    user = order_api.check_user(wechat_id)	
	    order = order_api.change_dinner_order(user,"spicy",True)
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'预定辣餐成功，查看订单', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/view_order/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)

	if event == "not_spicy":
	    user = order_api.check_user(wechat_id)
            order = order_api.change_dinner_order(user,"not_spicy",True)
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'预定不辣成功，查看订单', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/view_order/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)

	if event == "vegetable":
	    user = order_api.check_user(wechat_id)
            order = order_api.change_dinner_order(user,"vegetable",True)
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'预定素餐成功，查看订单', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/view_order/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)

	if event == "not_eat":
	    user = order_api.check_user(wechat_id)
            order = order_api.change_dinner_order(user,"not_spicy",False)
            news_message = message.NewsMessage(wechat_id, corp_id, timestamp, [{'title':'取消今日晚餐成功，查看订单', 'picurl': 'http://223.202.85.88/static/image/hungry.jpg','url': 'http://223.202.85.88/view_order/' + wechat_id}])
            ret, msg = news_message.encrypt(nonce)
            return HttpResponse(msg)
	
	# 入职指引
        if event == 'entry':
            entry_response = wechat_response.EntryResponse(wechat_id, corp_id, timestamp, nonce)
            articles = [{'title':'入职指引', 'picurl': 'http://223.202.85.88/static/image/cloudin.jpg','url': 'http://223.202.85.88/entry'}]
            return entry_response.response(articles)
