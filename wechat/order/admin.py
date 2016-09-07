from django.contrib import admin
from .models import User
from .models import Order
from .models import Suggest


# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Suggest)
