#!/usr/bin/python
# encoding: utf-8
import urllib
import urllib2
import json
import simplejson
import sys
import datetime
import time
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
            touser = "hongli_dream"
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
    
    #to_user_name 是一个列表，可以给多个用户发，如果为空，则发给指定用户
    def send_title_message(self, to_user_name, title, content):
	touser = '|'.join(to_user_name)
	if len(to_user_name) == 0:
            touser = "an839274949"
	body = {
	    'agentid': self.agent_id,
            'touser': touser,
            'msgtype': 'news',
            'news': {
		"articles":[
		    {
			'title':title,
			'description':content
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

def remind():

    secrect = "C-iU0CxqP-p4HlghOwsx-WAVNezpej4dy4uzfK_hbytxaqmoYc8DBeVOeVNc_Qts"
    token = "d78qRYadHXqodcIHVG6"
    encoding_aes_key = "JggEi7IHuUxjHSU9iBdRlfdsDORUFCrpUBhATVd4DM1"
    corp_id = "wxf3a0725934f1b55c"
    agent_id = '16'
    api = WechatAPI(token, encoding_aes_key, corp_id, secrect, agent_id)

    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f = open ('metting_durty_name','r')
    user_name = f.read()
    user_name = user_name.strip('\n')
    f.close()
    f = open ('next_metting_durty_name','r')
    next_user = f.read()
    next_user = next_user.strip('\n')
    f.close()
    user_list = api.get_user_list('3','1','0')["userlist"]
    flag = 0
    count = 0
    to_user = []
    #test_user = "an839274949"
    #to_user.append(str(test_user))
    for user in user_list:
        # 如果在去除列表中则不推送
        #if user["userid"] in exclude:
        #    continue
	count = count + 1
	user_n = user['name']
	if user_n == user_name:
	    flag = count
        wechat_id = user['userid']
	#print wechat_id
	to_user.append(str(wechat_id))
    if flag == len(user_list):
	flag = 0
    if user_list[flag]['name'] == "曹贝":
	flag = flag + 1
    #if user_list[flag]['name'] == "安鹏程":
#	flag = flag + 1
    if next_user  == "":
        next_user = user_list[flag]['name']
    f = open ('metting_durty_name','w')
    f.write(next_user)
    f.close()
    title = "周会值日生提醒\n"
    contest_pre = title + "本次周会值日生为："+user_name+"\n下次周会值日生为："+next_user+"\n请不能参加周会的同学及时请假\n"
    contest = contest_pre + "值日生工作内容：\n一、预定会议室(周五下午6点半)\n二、周报更新情况：\n   1、任务延期情况\n   2、任务拆分粒度\n   3、任务安排不清晰情况(如：目标，优先级等)\n   4、任务调整情况\n三、问题面板更新情况标记\n四、如遇月底或月初，check月总结和规划"
    #print to_user,contest

    api.send_title_message(to_user,str(title),str(contest))
    #common.admin_api.send_message(to_user,str(contest))

if __name__ == '__main__':
    remind()

    ## 下面这些是我们微信公众号的配置，不用改，直接用
    #secrect = "C-iU0CxqP-p4HlghOwsx-WAVNezpej4dy4uzfK_hbytxaqmoYc8DBeVOeVNc_Qts"
    #token = "d78qRYadHXqodcIHVG6"
    #encoding_aes_key = "JggEi7IHuUxjHSU9iBdRlfdsDORUFCrpUBhATVd4DM1"
    #corp_id = "wxf3a0725934f1b55c"
    ## 微信平台的报警应用id
    #agent_id = '16'
    #api = WechatAPI(token, encoding_aes_key, corp_id, secrect, agent_id)
    #ans = api.send_message(["hongli_dream",'houjincheng1992'], "报警了！！！")
    #print ans
