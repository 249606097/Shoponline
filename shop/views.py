from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings

from PIL import Image

from .forms import *
from .models import *

import datetime
import re
import random
import string
import os


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
        result = Cookie.objects.filter(key=cookie)
        if len(result) != 0:
            username = result[0].name
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
    elif len(User.objects.filter(name=username)) != 0:
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
            user_to_save = User(name=username,
                                password=encrypted_password,
                                answer=encrypted_answer,
                                type=user_type)
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
            user = User.objects.filter(name=username)
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
                cookie_to_save = Cookie(user_name=username,
                                        key=random_string)
                cookie_to_save.save()
                return response


def edit(request):
    return render(request, "Add.html")


def add(request):
    good_name = request.POST.get('good_name')
    good_price = request.POST.get('good_price')
    description = request.POST.get('content')
    user = User.objects.get(id=1)  # 先默认
    good_to_save = Goods(name=good_name,
                         number=1,
                         version=1,
                         amount=0,
                         turnover=0,
                         status=0,
                         description=description,
                         price=good_price,
                         seller=user,
                         put_on_time=timezone.now())
    good_to_save.save()
    # return render(request, "Add.html", {"content": content})
    return render(request, "show.html", {"html": description})


def goods_list(request):
    goods = Goods.objects.all()
    return render(request, "GoodsList.html", {"goods": goods})


def edit_good(request):
    form = CaptchaForm()
    return render(request, 'EditGood.html', {"form": form})


# 富文本编辑器上传图片
@csrf_exempt
def upload(request):
    try:
        file = request.FILES['image']
        img = Image.open(file)
        img.thumbnail((500, 500), Image.ANTIALIAS)
        extension = os.path.splitext(file.name)[1]
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = random.randint(0, 999999)
        file_name = str(now_time) + str(random_number).zfill(6)

        try:
            img.save(settings.IMAGE_ROOT[0] + file_name + extension, img.format)
        except:
            print("img.save error")
        # 图片的name和format都是动态获取的，支持png，jpeg，gif等

        # 注意此处 注意此处 注意此处 注意此处 注意此处 注意此处 注意此处
        path = settings.MEDIA_ROOT + file_name + extension
        # 注意此处 注意此处 注意此处 注意此处 注意此处 注意此处 注意此处

        # return HttpResponse(
        #     "<script>top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val('%s').closest('.mce-window').find('.mce-primary').click();</script>" % path)

        return HttpResponse(
            "<script>top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val('"
            + "/../.." + path +
            "').closest('.mce-window').find('.mce-primary').click();</script>")
    except Exception:
        return HttpResponse("error")


def number_test(number):
    if len(number) == 0:
        result = "请输入数据"
        return result
    # elif not re.search(r'^[-+]?[0-9]+\.?[0-9]+$', number):
    elif not re.search(r'^[0-9]+\.?[0-9]+$', number):
        result = "请输入正确的数据"
        return result
    else:
        result = True
        return result


def name_test(name):
    if len(name) == 0:
        result = "请输入商品名"
        return result
    else:
        return True


@csrf_exempt
def create_good(request):
    form = CaptchaForm(request.POST)

    name = request.POST.get('name')
    price = request.POST.get('price')
    amount = request.POST.get('amount')
    description = request.POST.get('description')

    good = {"name": name, "price": price, "amount": amount, "description": description}

    result = name_test(name)
    if result is not True:
        form = CaptchaForm()
        return render(request, "EditGood.html", {"result": result, "form": form, "good": good})

    result = number_test(price)
    if result is not True:
        form = CaptchaForm()
        return render(request, "EditGood.html", {"result": result, "form": form, "good": good})

    result = number_test(amount)
    if result is not True:
        form = CaptchaForm()
        return render(request, "EditGood.html", {"result": result, "form": form, "good": good})

    if not form.is_valid():
        result = "验证码错误"
        form = CaptchaForm()
        return render(request, "EditGood.html", {"result": result, "form": form, "good": good})

    file = request.FILES.get('img')

    if file is None:
        path = settings.MEDIA_ROOT + 'default.gif'
    else:
        picture = Image.open(request.FILES.get('img'))
        picture.thumbnail((200, 200), Image.ANTIALIAS)  # 设置图片的长宽度 抗锯齿

        # 商品头像的图片 文件名的生成 保存
        extension = os.path.splitext(file.name)[1]
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = random.randint(0, 999999)
        file_name = str(now_time) + str(random_number).zfill(6)
        path = settings.MEDIA_ROOT + file_name + extension

        picture.save(settings.IMAGE_ROOT[0] + file_name + extension, picture.format)

    # 数据库image的在 html 的显示代码
    # <p><img src="static/img/default.gif" alt="" width="200" height="200"/></p>
    picture_url = '<p><img src="' + path + '" alt="" width="200" height="200"/></p>'

    number = request.POST.get('number')

    good = Goods.objects.filter(number=number)
    if len(good) != 0:
        good = good[0]
        version = str(int(good.version) + 1)
        old_good_to_save = OldGoods(number=good.number,
                                    version=good.version,
                                    seller=good.seller,
                                    name=good.name,
                                    price=good.price,
                                    image=good.image,
                                    description=good.description,
                                    create_time=good.create_time,
                                    put_on_time=good.put_on_time)
        old_good_to_save.save()

        good.version = version
        good.name = name
        good.price = price
        good.amount = amount
        good.image = picture_url
        good.description = description
        good.put_on_time = timezone.now()
        good.save()

    else:
        # 新商品 生成
        number_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        number_random = random.randint(0, 999999)
        number = str(number_time) + str(number_random).zfill(6)

        seller = User.objects.get(id=1)  # 默认
        good_to_save = Goods(name=name,
                             price=price,
                             amount=amount,
                             description=description,
                             number=number,
                             version=1,
                             seller=seller,
                             turnover=0,
                             status=0,
                             put_on_time=timezone.now(),
                             image=picture_url)
        good_to_save.save()
    return render(request, "Welcome.html", {"description": description})


def good_page(request, number):
    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html", {})
    else:
        good.order_by('version')
        good = good[0]
        return render(request, "GoodPage.html", {"good": good})


def jump_to_none(request):
    return render(request, "NOPage.html")


def re_edit(request, number):
    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html", {})
    else:
        good.order_by('version')
        good = good[0]
        form = CaptchaForm()
        return render(request, "EditGood.html", {"good": good, "form": form})


def delete_good(request, number):
    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")

    good = good[0]
    old_good_to_save = OldGoods(number=good.number,
                                version=good.version,
                                seller=good.seller,
                                name=good.name,
                                price=good.price,
                                image=good.image,
                                description=good.description,
                                create_time=good.create_time,
                                put_on_time=good.put_on_time)
    old_good_to_save.save()

    good.delete()
    return render(request, "Welcome.html", {})





