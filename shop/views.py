from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
import re
import random
import string


def jump_to_welcome_page(request):
    return render(request, "Welcome.html")


def clean_cookie():
    all_cookie = Cookie.objects.all()
    for one in all_cookie:
        if one.cookie_create_time.replace(tzinfo=None) + datetime.timedelta(hours=8, minutes=10) < \
                datetime.datetime.now().replace(tzinfo=None):
            one.delete()


def check_cookie(request):
    clean_cookie()
    if not request.COOKIES.get("key"):
        pass
    else:
        cookie = request.COOKIES.get("key")
        result = Cookie.objects.filter(cookie_key=cookie)
        if len(result) != 0:
            username = result[0].cookie_user_name
            return username


def username_test(username):
    if len(username) < 6:
        result = "用户名必须不少于6个字符"
        return result
    elif re.search(r'\W', username) or re.search(r'[A-Z]', username):
        result = "用户名只能由数字、小写字母或下划线组成"
        return result
    elif re.search(r'^_', username) or re.search(r'_$', username):
        result = "用户名不能以下划线开头或结尾"
        return result
    elif re.search(r' ', username):
        result = "用户名不能含有空格"
        return result
    elif len(User.objects.filter(user_name=username)) != 0:
        result = "用户名已经被注册"
        return result
    else:
        result = True
        return result


def password_test(password, password_re):
    if len(password) < 6:
        result = "密码必须不少于6个字符"
        return result
    elif re.search(r' ', password):
        result = "密码不能含有空格"
        return result
    elif not re.search(r'[a-zA-Z]', password) and re.search(r'[0-9]', password):
        result = "密码必须含有数字和字母"
        return result
    elif password != password_re:
        result = "两次输入的密码不同"
        return result
    else:
        result = True
        return result


def answer_test(answer):
    result = "密保问题答案不符合规定"
    if len(answer) != 8:
        return result
    elif re.search(r'\D', answer):
        return result
    else:
        result = True
        return result


def register(request):
    if request.method != "POST":
        form = RegisterForm()
        return render(request, "RegisterPage.html", {"form": form})
    else:
        form = RegisterForm(request.POST)
        if not form.is_valid():
            result = "验证码错误"
            return render(request, "RegisterPage.html", {"form": form, "result": result})
        else:
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password_re = form.cleaned_data["password_re"]
            answer = form.cleaned_data["answer"]
            user_type = form.cleaned_data["user_type"]
            result = username_test(username)
            if result is not True:
                return render(request, "RegisterPage.html", {"form": form, "result": result})
            result = password_test(password, password_re)
            if result is not True:
                return render(request, "RegisterPage.html", {"form": form, "result": result})
            result = answer_test(answer)
            if result is not True:
                return render(request, "RegisterPage.html", {"form": form, "result": result})
            encrypted_password = make_password(password)
            encrypted_answer = make_password(answer)
            user_to_save = User(user_name=username,
                                user_password=encrypted_password,
                                user_answer=encrypted_answer,
                                user_type=user_type)
            user_to_save.save()
            return HttpResponseRedirect(reverse('shop:welcome'))


def login(request):
    if request.method != "POST":
        form = LoginForm()
        return render(request, "LoginPage.html", {"form": form})
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            result = "验证码错误"
            return render(request, "LoginPage.html", {"form": form, "result": result})
        else:
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(user_name=username)
            if len(user) == 0:
                result = "用户不存在"
                return render(request, "LoginPage.html", {"form": form, "result": result})
            elif not check_password(password, user[0].user_password):
                result = "密码错误"
                return render(request, "LoginPage.html", {"form": form, "result": result})
            else:
                random_string = ''.join(random.sample(string.ascii_letters + string.digits, 30))
                response = HttpResponseRedirect(reverse('shop:welcome'))
                response.set_cookie("key", random_string, 3600, '/')
                cookie_to_save = Cookie(cookie_user_name=username,
                                        cookie_key=random_string)
                cookie_to_save.save()
                return response
