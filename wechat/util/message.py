import common
class BaseMessage(object):
    def __init__(self, to_user_name, from_user_name, timestamp):
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.timestamp = timestamp

    def encrypt(self, nonce):
        xml = self.get_xml()
        return common.wxcpt.EncryptMsg(xml, nonce, self.timestamp)

    def get_xml(self):
        msg_xml = ""
        msg_xml += "<xml>"
        msg_xml += "<ToUserName><![CDATA[" + self.to_user_name + "]]></ToUserName>"
        msg_xml += "<FromUserName><![CDATA[" + self.from_user_name + "]]></FromUserName>"
        msg_xml += "<CreateTime>" + self.timestamp + "</CreateTime>"
        return msg_xml

class NewsMessage(BaseMessage):
    def __init__(self, to_user_name, from_user_name, timestamp, articles):
        super(NewsMessage, self).__init__(to_user_name, from_user_name, timestamp)
        self.articles = articles

    def get_xml(self):
        xml = super(NewsMessage, self).get_xml()
        xml += "<MsgType><![CDATA[news]]></MsgType>"
        xml += "<ArticleCount>%s</ArticleCount>" % str(len(self.articles))
        xml += "<Articles>"
        for article in self.articles:
            xml += "<item>"
            if 'title' in article:
                xml += "<Title><![CDATA[%s]]></Title>" % article['title']
            if 'description' in article:
                xml += "<Description><![CDATA[%s]]></Description>" % article['description']
            if 'picurl' in article:
                xml += "<PicUrl><![CDATA[%s]]></PicUrl>" % article['picurl']
            if 'url' in article:
                xml += "<Url><![CDATA[%s]]></Url>" % article['url']
            xml += "</item>"
        xml += "</Articles>"
        xml += "</xml>"
        return xml

class TextMessage(object):
    def __init__(self, to_user_name, from_user_name, timestamp, content, agent_id):
        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.timestamp = timestamp
        self.content = content
        self.agent_id = agent_id

    def get_xml(self):
        msg_xml = ""
        msg_xml += "<xml>"
        msg_xml += "<ToUserName><![CDATA[" + self.to_user_name + "]]></ToUserName>"
        msg_xml += "<FromUserName><![CDATA[" + self.from_user_name + "]]></FromUserName>"
        msg_xml += "<CreateTime>" + self.timestamp + "</CreateTime>"
        msg_xml += "<MsgType><![CDATA[text]]></MsgType>"
        msg_xml += "<Content><![CDATA[" + self.content + "]]></Content>"
        msg_xml += "<AgentID>" + self.agent_id + "</AgentID>"
        msg_xml += "</xml>"
        return msg_xml
