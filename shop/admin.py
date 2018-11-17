from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_password', 'user_answer', 'user_type')


admin.site.register(User, UserAdmin)
