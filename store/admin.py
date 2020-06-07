from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(product_DB)
admin.site.register(cart_DB)
admin.site.register(order_DB)
admin.site.register(user_DB)