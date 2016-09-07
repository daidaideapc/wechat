#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Role(object):
    def __init__(self):
        self.permissions = set()

    def has_permission(self, permission):
        return permission in self.permissions

class BaseRole(Role):
    def __init__(self):
        super(BaseRole, self).__init__()
        self.permissions.add('base')

class OrderAdmin(BaseRole):
    def __init__(self):
        super(OrderAdmin, self).__init__()
        self.permissions.add('admin_order')

base_role = BaseRole()
order_admin = OrderAdmin()
