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
    user_type = fields.ChoiceField(label="用户类型",
                                   initial=1,
                                   choices=((1, '买家'), (2, '卖家')))
    captcha = CaptchaField(label="验证码")

    # def clean_password(self):
    #     raw_password = self.cleaned_data.get('password')
    #     pass
    #     return raw_password


class LoginForm(forms.Form):
    username = fields.CharField(widget=widgets.TextInput,
                                label="用户")
    password = fields.CharField(widget=widgets.PasswordInput,
                                label="密码")
    captcha = CaptchaField(label="验证码")














