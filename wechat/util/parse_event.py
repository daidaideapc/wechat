#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xml.etree.cElementTree as ET

# 解析用户动作
def parse_event(xml_tree):
    user = xml_tree.find("FromUserName").text

    if xml_tree.find("Event") != None:
        event = xml_tree.find("Event").text
        # 关注微信号
        if event == "subscribe":
            return "subscribe"
        # 取关微信号
        if event == "unsubscribe":
            return "unsubscribe"

    if xml_tree.find("EventKey") != None and xml_tree.find("Event") != None:
        event = xml_tree.find("Event").text
        event_key = xml_tree.find("EventKey").text
        if event == "click":
            # 订餐设置
            if event_key == "1_1":
                return "order_setting"
            # 查看订餐情况
            if event_key == "2_1":
                return "view_order"
            ## 订餐反馈
            #if event_key == "2_6":
            #    return "order_suggest"
            ## 查看反馈
            #if event_key == "2_7":
            #    return "suggest_view"
            # 订餐表单页面
            if event_key == 'spicy':
                return "spicy"
	    if event_key == 'not_spicy':
    		return "not_spicy"
 	    if event_key == 'vegetable':
    		return "vegetable"
	    if event_key == 'not_eat':
		return "not_eat"
            # 入职指引
            if event_key == '2_1_1':
                return "entry"
    return None
