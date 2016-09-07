#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.
class User(models.Model):
    # 微信账号
    wechat_id = models.CharField(max_length=50, primary_key=True)
    # 姓名
    name = models.CharField(max_length=30)
    # 部门id，字符串形式，多个id用空格分隔 默认是1
    department_id = models.CharField(max_length=10, default='1')
    # 职位
    position = models.CharField(max_length=30, blank=True)
    # 手机
    mobile = models.CharField(max_length=20, blank=True)
    # 性别 '1': 男性 '2': 女性
    gender = models.CharField(max_length=1, blank=True)
    # 邮箱
    email = models.EmailField(max_length=254, blank=True)
    # 头像media_id
    avatar_mediaid = models.CharField(max_length=100, blank=True)
    # 附加属性，一个json串
    extattr = models.CharField(max_length=1000, blank=True)
    # 默认是否点餐
    default_order = models.BooleanField(default=True)
    # 辣、不辣还是吃素
    order_category = models.CharField(max_length=100, default="not_spicy", blank=True)
    # 角色列表
    role_list = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, related_name='user_order')
    # 午餐、晚餐
    order_type = models.CharField(max_length=100)
    # 吃还是不吃
    eat = models.BooleanField(default=True)
    # 清淡、辣、不辣
    category = models.CharField(max_length=100, default="not_spicy")
    # 日期
    date = models.DateField()
    def __unicode__(self):
        return str(self.date) + "\t" + self.user.name + "\t" + self.order_type

class Suggest(models.Model):
    user = models.ForeignKey(User, related_name='user_suggest')
#    # 微信账号
#    wechat_id = models.CharField(max_length=50, primary_key=True)
    # 标题
    title = models.CharField(max_length=30, default="")
    # 建议正文
    suggest_text = models.CharField(max_length=1000)
    # 回复
    reply = models.CharField(max_length=1000, blank=True)
    # 日期
    date = models.DateField()
    def __unicode__(self):
        return self.title


