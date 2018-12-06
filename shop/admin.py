from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'answer', 'type')


class GoodAdmin(admin.ModelAdmin):
    list_display = ()


admin.site.register(User, UserAdmin)
admin.site.register(Goods)
admin.site.register(DetailList)
admin.site.register(Comment)
