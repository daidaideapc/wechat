# encoding: utf-8
import urllib
import urllib2
import message
import json
import simplejson
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class WechatAPI(object):
    def __init__(self, token, encoding_aes_key, corp_id, secrect, agent_id):
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.corp_id = corp_id
        self.secrect = secrect
        self.agent_id = agent_id

    # 获取access_token，用于之后的一些主动操作，例如主动给某个用户发送消息
    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + self.corp_id + "&corpsecret=" + self.secrect
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        access_token = json.loads(response.read())["access_token"]
        return access_token

    # to_user_name是一个列表，可以给多个用户发，如果"@all"表示给所有用户发消息
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
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        return json.loads(response.read())["errmsg"] == "ok"


if __name__ == '__main__':
    # 下面这些是我们微信公众号的配置，不用改，直接用
    secrect = "C-iU0CxqP-p4HlghOwsx-WAVNezpej4dy4uzfK_hbytxaqmoYc8DBeVOeVNc_Qts"
    token = "d78qRYadHXqodcIHVG6"
    encoding_aes_key = "JggEi7IHuUxjHSU9iBdRlfdsDORUFCrpUBhATVd4DM1"
    corp_id = "wxf3a0725934f1b55c"
    # 微信平台的报警应用id
    agent_id = '6'
    api = WechatAPI(token, encoding_aes_key, corp_id, secrect, agent_id)
    api.send_message(["cugb15201017684"], "报警了！！！")
