from django import forms
from django.forms import widgets
from django.forms import fields
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    username = fields.CharField(widget=widgets.TextInput,
                                label="用户")
    password = fields.CharField(widget=widgets.PasswordInput,
                                label="密码")
    password_re = fields.CharField(widget=widgets.PasswordInput,
                                   label="再次输入密码")
    answer = fields.CharField(widget=widgets.TextInput,
                              label="密保问题答案")
    captcha = CaptchaField()

















