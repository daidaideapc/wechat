#-*- encoding:utf-8 -*-
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from order import order_api

# Create your tests here.

def output(ans):
    for k in ans:
        try:
            order_list = ans[k]
            for order in order_list:
                print order.date, order.user.name, order.category, order.order_type, order.eat
        except:
            print k, ans[k]
    print("\n")

class OrderTest(TestCase):
    #测试非成员
    def test_new_user(self):
        user = order_api.check_user("we8449875098")
        print type(user)
        print "\n"

    #测试成员与非成员订单视图
    def test_order_view_not_member(self):
        user = "we8449875098"
        ans = order_api.order_view({},user)
        output(ans)
        print "\n"

    def test_order_view_member(self):
        user = "an839274949"
        ans = order_api.order_view({},user)
        output(ans)
        print "\n"


    # 测试成员与非成员订餐获取
    def test_order_form_get_not_member(self):
        user = "we8449875098"
        ans = order_api.order_form_get({},user)
        output(ans)
        print "\n"


    def test_order_form_get_member(self):
        user = "an839274949"
        ans = order_api.order_form_get({},user)
        output(ans)
        print "\n"


    #测试成员与非成员订餐结果
    def test_order_form_post_member1(self):
        user = "an839274949"
        post = {'lunch_order_date':'2015 November 2','dinner_order_date':'2015 November 2','lunch_radios':'not_eat','dinner_radios':'meat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        post = {'lunch_order_date':'2015 November 3','dinner_order_date':'2015 November 3','lunch_radios':'eat','dinner_radios':'meat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        post = {'lunch_order_date':'2015 November 4','dinner_order_date':'2015 November 4','lunch_radios':'not_eat','dinner_radios':'vegetable'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        post = {'lunch_order_date':'2015 November 5','dinner_order_date':'2015 November 5','lunch_radios':'eat','dinner_radios':'vegetable'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        post = {'lunch_order_date':'2015 November 6','dinner_order_date':'2015 November 6','lunch_radios':'not_eat','dinner_radios':'not_eat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        post = {'lunch_order_date':'2015 November 7','dinner_order_date':'2015 November 7','lunch_radios':'eat','dinner_radios':'not_eat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        ans = order_api.order_view({},user)
        output(ans)
        print "\n"

    def test_order_form_post_not_member(self):
        user = "we8449875098"
        post = {'lunch_order_date':'2015 November 2','dinner_order_date':'2015 November 2','lunch_radios':'eat','dinner_radios':'meat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_form_post(request,user)
        ans = order_api.order_view({},user)
        output(ans)
        print "\n"



    #测试成员与非成员订餐设置
    def test_order_setting_not_member(self):
        user = "we8449875098"
        ans = order_api.order_setting_get({},user)
        output(ans)
        post = {'auto_order':False,'default_category':'meat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_setting_post(request,user)
        output(ans)
        ans = order_api.order_setting_get({},user)
        output(ans)
        print "\n"


    def test_order_setting_member(self):
        user = "an839274949"
        ans = order_api.order_setting_get({},user)
        output(ans)

        post = {'auto_order':True,'default_category':'meat'}
        request = HttpRequest()
        request.POST = post
        request.methon = 'POST'
        ans = order_api.order_setting_post(request,user)
        output(ans)

        ans = order_api.order_setting_get({},user)
        output(ans)

        post = {'auto_order':True,'default_category':'vegetable'}
        request.POST = post
        ans = order_api.order_setting_post(request,user)
        output(ans)

        ans = order_api.order_setting_get({},user)
        output(ans)

        post = {'auto_order':False,'default_category':'meat'}
        request.POST = post
        ans = order_api.order_setting_post(request,user)
        output(ans)

        ans = order_api.order_setting_get({},user)
        output(ans)

        post = {'auto_order':False,'default_category':'vegetable'}
        request.POST = post
        ans = order_api.order_setting_post(request,user)
        output(ans)

        ans = order_api.order_setting_get({},user)
        output(ans)
