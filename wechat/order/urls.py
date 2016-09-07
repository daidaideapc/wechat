from django.conf.urls import url

from views import order_setting
from views import order_form
from views import views
from views import view_order
from views import order_suggest
from views import suggest_view
from views import suggest_reply

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^order_form/(?P<wechat_id>\w+)$', order_form.order_form, name='order_form'),
  url(r'^order_suggest/(?P<wechat_id>\w+)$', order_suggest.order_suggest, name='order_suggest'),
  url(r'^suggest_reply/(?P<wechat_id>\w+)/(?P<suggest_id>\d+)$', suggest_reply.suggest_reply, name='suggest_reply'),
  url(r'^suggest_view/(?P<wechat_id>\w+)$', suggest_view.suggest_view, name='suggest_view'),
  url(r'^entry$', views.entry, name='entry'),
  url(r'^order_setting/(?P<wechat_id>\w+)$', order_setting.order_setting, name='order_setting'),
  url(r'^view_order/(?P<wechat_id>\w+)$', view_order.view_order, name='view_order'),
]
