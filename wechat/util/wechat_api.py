# encoding: utf-8
import urllib
import urllib2
import json
import simplejson
import sys
import ssdb_client
import unittest
import time
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

class WechatAPI(object):
    def __init__(self, token, encoding_aes_key, corp_id, secrect, agent_id):
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.corp_id = corp_id
        self.secrect = secrect
        self.agent_id = agent_id
        # 使用ssdb作为access_token的缓存
        self.ssdb = ssdb_client.SSDBClient("127.0.0.1", 8888)

    # 获取access_token，用于之后的一些主动操作，例如主动给某个用户发送消息
    def get_access_token(self):
        # 先尝试从ssdb取access_token
        success, data = self.ssdb.get("access_token")
        # 如果成功直接返回
        if success:
            return data
        # 不成功就要重新取
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + self.corp_id + "&corpsecret=" + self.secrect
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        try:
            access_token = json.loads(response.read())["access_token"]
            # 存到ssdb上，过期时间设为7200s
            self.ssdb.setx("access_token", access_token, 7200)
            return access_token
        except:
            return None

    # to_user_name是一个列表，可以给多个用户发，如果为空表示给所有用户发消息
    def send_message(self, to_user_name, msg):
        touser = '|'.join(to_user_name)
        if len(to_user_name) == 0:
            touser = "@all"
        # toparty和totag可以为空，暂时用不到
        #"toparty": " PartyID1 | PartyID2 ",
        #"totag": " TagID1 | TagID2 ",
        body = {
            'agentid': self.agent_id,
            'touser': touser,
            'msgtype': 'text',
            'text': {
                'content': msg
            },
            'safe': '0'
        }
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_access_token()
        data = json.dumps(body, ensure_ascii=False)
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "   " + data
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
	res = response.read()
        return json.loads(res)["errmsg"] == "ok"
 
    # to_user_name是一个列表，可以给多个用户发，如果为空表示给所有用户发消息
    def send_test_message(self, to_user_name, title, contest):
        touser = '|'.join(to_user_name)
        if len(to_user_name) == 0:
            touser = "an839274949"
        # toparty和totag可以为空，暂时用不到
        #"toparty": " PartyID1 | PartyID2 ",
        #"totag": " TagID1 | TagID2 ",
        body = {
            'agentid': self.agent_id,
            'touser': touser,
            'msgtype': 'news',
            'news': {
		'articles':[
		    {
			'title':title,
			'description':contest,
		    }
		]
            },
            'safe': '0'
        }
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_access_token()
        data = json.dumps(body, ensure_ascii=False)
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "   " + data
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
	res = response.read()
        return json.loads(res)["errmsg"] == "ok"

    def send_news_message(self, to_user_name, articles):
        touser = '|'.join(to_user_name)
        if len(to_user_name) == 0:
            touser = "@all"
        body = {
            'agentid': self.agent_id,
            'touser': touser,
            'msgtype': 'news',
            'news': {
                'articles': articles
            }
        }
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.get_access_token()
        data = json.dumps(body, ensure_ascii=False)
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "   " + data
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        res = response.read()
        return json.loads(res)["errmsg"] == "ok"

    '''
    返回一个用户信息词典
    {
       "errcode": 0, 返回码
       "errmsg": "ok", 对返回码的文本描述内容
       "userid": "zhangsan", 成员UserID。对应管理端的帐号
       "name": "李四", 成员名称
       "department": [1, 2], 成员所属部门id列表
       "position": "后台工程师", 职位信息
       "mobile": "15913215421", 手机号
       "gender": "1", 性别。0表示未定义，1表示男性，2表示女性
       "email": "zhangsan@gzdev.com", 邮箱
       "weixinid": "lisifordev", 微信号
       头像url。注：如果要获取小图将url最后的"/0"改成"/64"即可
       "avatar": "http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0",
       "status": 1, 关注状态: 1=已关注，2=已冻结，4=未关注
       "extattr": {"attrs":[{"name":"爱好","value":"旅游"},{"name":"卡号","value":"1234567234"}]} 扩展属性
    }
    '''
    def get_user_info(self, user_id):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=" + self.get_access_token() + "&userid=" + user_id
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        user_info = json.loads(response.read())
        if user_info['errmsg'] != "ok":
            user_info = None
        return user_info

    '''
    返回json字典
    {
        "errcode": 0,
        "errmsg": "ok",
        "userlist": [
           {
               "userid": "lisi",
               "name": "李四",
               "department": [1, 2]
           },
           {
               "userid": "zhangsan",
               "name": "张三",
               "department": [1, 2]
           },
       ]
    }
    department_id 部门id
    fetch_child 1表示递归查找，0不递归
    status 0获取全部成员，1获取已关注成员列表，2获取禁用成员列表，4获取未关注成员列表
    '''
    def get_user_list(self, department_id='1', fetch_child='1', status='0'):
        access_token = self.get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=" + access_token + \
                "&department_id=" + department_id + \
                "&fetch_child=" + fetch_child + \
                "&status=" + status
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        user_list = json.loads(response.read())
        if user_list['errmsg'] != 'ok':
            user_list = None
        return user_list


class WechatAPITestCase(unittest.TestCase):
    def setUp(self):
        secrect = "C-iU0CxqP-p4HlghOwsx-WAVNezpej4dy4uzfK_hbytxaqmoYc8DBeVOeVNc_Qts"
        token = "d78qRYadHXqodcIHVG6"
        encoding_aes_key = "JggEi7IHuUxjHSU9iBdRlfdsDORUFCrpUBhATVd4DM1"
        corp_id = "wxf3a0725934f1b55c"
        agent_id = '3'
        self.api = WechatAPI(token, encoding_aes_key, corp_id, secrect, agent_id)

    def test_get_access_token(self):
        self.assertTrue(self.api.get_access_token() != None)

    def test_send_message(self):
        self.assertTrue(self.api.send_message(["cugb15201017684"], "test"))

    def test_send_news_message(self):
        self.assertTrue(self.api.send_news_message(['cugb15201017684'], [{'title':'Title', 'description':'Des', 'picurl':'http://img1.cache.netease.com/catchpic/C/CC/CCC8117C8E338E550C2C49B6AD611C4D.jpg', 'url': 'http://www.baidu.com'},{'title':'Title', 'description':'Des', 'picurl':'http://img1.cache.netease.com/catchpic/C/CC/CCC8117C8E338E550C2C49B6AD611C4D.jpg', 'url': 'http://180.97.185.116/order_form/cugb15201017684'}]))

    def test_get_user_info(self):
        self.assertTrue(self.api.get_user_info("cugb15201017684") != None)

    def test_get_user_list(self):
        self.assertTrue(self.api.get_user_list() != None)

if __name__ == '__main__':
    unittest.main()
