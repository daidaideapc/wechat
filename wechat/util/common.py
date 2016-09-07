#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sys
sys.path.append('../')
import wechat_api
from wechat import settings
import datetime
from WXBizMsgCrypt import WXBizMsgCrypt
reload(sys)
sys.setdefaultencoding('utf-8')

# 行政
admin_api = wechat_api.WechatAPI(settings.token,
                                 settings.encoding_aes_key,
                                 settings.corp_id,
                                 settings.secrect,
                                 settings.admin_agent_id)

#hr
hr_api = wechat_api.WechatAPI(settings.token,
                              settings.encoding_aes_key,
                              settings.corp_id,
                              settings.secrect,
                              settings.hr_agent_id)

# 微信加密解密接口
wxcpt = WXBizMsgCrypt(settings.token, settings.encoding_aes_key, settings.corp_id)

def string_to_date(s):
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    tokens = s.split(' ')
    if len(tokens) == 3:
        return datetime.date(int(tokens[0]), month_map[tokens[1]], int(tokens[2]))

def date_to_string(d):
    month_map = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return str(d.year) + " " + month_map[d.month] + " " + str(d.day)

if __name__ == '__main__':
    print "ok"
