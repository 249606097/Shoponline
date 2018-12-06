from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
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
        if one.create_time.replace(tzinfo=None) + datetime.timedelta(hours=8, minutes=10) < \
                datetime.datetime.now().replace(tzinfo=None):
            one.delete()


def check_cookie(request):
    clean_cookie()
    if not request.COOKIES.get("key"):
        return False
    else:
        cookie = request.COOKIES.get("key")
        result = Cookie.objects.filter(key=cookie)
        if len(result) != 0:
            username = result[0].user_name
            return username
        else:
            return False


def welcome(request):
    man = check_cookie(request)
    login_authority = "hidden"
    un_login_authority = "hidden"
    seller_authority = "hidden"
    buyer_authority = "hidden"
    if man is False:
        man = "游客"
        un_login_authority = ""
        return render(request, "Welcome.html", {"man": man,
                                                "login_authority": login_authority,
                                                "un_login_authority": un_login_authority,
                                                "seller_authority": seller_authority,
                                                "buyer_authority": buyer_authority})
    else:
        login_authority = ""
        user = User.objects.filter(name=man)
        if user[0].type == 2:
            seller_authority = ""
        if user[0].type == 1:
            buyer_authority = ""
        return render(request, "Welcome.html", {"man": man,
                                                "login_authority": login_authority,
                                                "un_login_authority": un_login_authority,
                                                "seller_authority": seller_authority,
                                                "buyer_authority": buyer_authority
                                                })


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
    man = check_cookie(request)
    if man is not False:
        return HttpResponseRedirect(reverse('shop:welcome'))

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
            elif not check_password(password, user[0].password):
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


def change_password(request):
    man = check_cookie(request)
    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            result = "验证码错误"
            return render(request, "ChangePassword.html", {"form": form, "result": result})
        else:
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            new_password_re = form.cleaned_data["new_password_re"]
            result = password_test(new_password, new_password_re)
            if result is not True:
                return render(request, "ChangePassword.html", {"form": form, "result": result})
            user = User.objects.filter(name=man)[0]
            if not check_password(old_password, user.password):
                result = "密码错误"
                return render(request, "ChangePassword.html", {"form": form, "result": result})
            else:
                encrypted_password = make_password(new_password)
                user.password = encrypted_password
                user.save()
                result = "修改成功"
                return render(request, "ChangePassword.html", {"form": form, "result": result})

    else:
        form = ChangePasswordForm()
        return render(request, "ChangePassword.html", {"form": form})


def forget_password(request):
    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        if not form.is_valid():
            result = "验证码错误"
            return render(request, "ForgetPassword.html", {"form": form, "result": result})
        else:
            username = form.cleaned_data["username"]
            answer = form.cleaned_data["answer"]
            new_password = form.cleaned_data["new_password"]
            new_password_re = form.cleaned_data["new_password_re"]
            result = password_test(new_password, new_password_re)
            if result is not True:
                return render(request, "ForgetPassword.html", {"form": form, "result": result})
            else:
                user = User.objects.filter(name=username)
                if len(user) == 0:
                    result = "用户不存在"
                    return render(request, "ForgetPassword.html", {"form": form, "result": result})
                else:
                    if not check_password(answer, user[0].answer):
                        result = "密保问题答案错误"
                        return render(request, "ForgetPassword.html", {"form": form, "result": result})
                    else:
                        user = user[0]
                        encrypted_password = make_password(new_password)
                        user.password = encrypted_password
                        user.save()
                        result = "修改成功"
                        return render(request, "ForgetPassword.html", {"form": form, "result": result})
    else:
        form = ForgetPasswordForm()
        return render(request, "ForgetPassword.html", {"form": form})


def logout(request):
    man = check_cookie(request)
    if man is not False:
        cookie = Cookie.objects.filter(user_name=man)
        if len(cookie) == 0:
            pass
        else:
            cookie.delete()
    return HttpResponseRedirect(reverse('shop:welcome'))


def goods_list(request):
    goods = Goods.objects.filter(status=1)
    if request.method == "POST":
        order = request.POST.get("order")
        if order == "按价格 升序":
            goods = goods.order_by("price")
        if order == "按价格 降序":
            goods = goods.order_by("-price")
        if order == "按时间 升序":
            goods = goods.order_by("put_on_time")
        if order == "按时间 降序":
            goods = goods.order_by("-put_on_time")
    return render(request, "GoodsList.html", {"goods": goods})


def search(request):
    if request.method == "POST":
        keywords = request.POST.get("keywords")
        goods = Goods.objects.filter(status=1, name__icontains=keywords)
        return render(request, "SearchPage.html", {"goods": goods})


def edit_good(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    form = CaptchaForm()
    return render(request, 'EditGood.html', {"form": form})


# 富文本编辑器上传图片
@csrf_exempt
def upload(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

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
        #     "<script>top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val('%s').
        # closest('.mce-window').find('.mce-primary').click();</script>" % path)

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
    elif not (re.search(r'^[0-9]+\.?[0-9]+$', number) or re.search(r'^[0-9]+\.?[0-9]?$', number)):
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
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

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
    picture_url = '<p><img src="' + path + '" alt="" width="100" height="100"/></p>'

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

        seller = User.objects.get(name=man, type=2)
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
    return HttpResponseRedirect(reverse('shop:welcome'))


def good_page(request, number):
    man = check_cookie(request)
    good = Goods.objects.filter(number=number)

    seller_authority = "hidden"
    buyer_authority = "hidden"

    if len(good) == 0:
        return render(request, "NOPage.html", {})
    else:
        # good.order_by('version')
        good = good[0]
        if good.seller.name == man:
            seller_authority = ""
        buyer = User.objects.filter(name=man)
        if len(buyer) != 0 and buyer[0].type == 1:
            buyer_authority = ""
        comments = Comment.objects.filter(goods=good)
        no_comment = "无评论"
        if len(comments) != 0:
            no_comment = ""
        return render(request, "GoodPage.html", {"good": good,
                                                 "seller_authority": seller_authority,
                                                 "buyer_authority": buyer_authority,
                                                 "comments": comments,
                                                 "no_comment": no_comment})


def jump_to_none(request):
    return render(request, "NOPage.html")


def re_edit(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html", {})
    else:
        good.order_by('version')
        good = good[0]
        if good.seller.name != man:
            return HttpResponseRedirect(reverse('shop:welcome'))
        else:
            form = CaptchaForm()
            return render(request, "EditGood.html", {"good": good, "form": form})


def delete_good(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")

    if good[0].seller.name != man:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good_in_car = ShopCar.objects.filter(good=good)
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

    good_in_car.delete()
    good.delete()
    return HttpResponseRedirect(reverse('shop:welcome'))


def add_to_car(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")
    else:
        good = good[0]
        valid_confirm = ShopCar.objects.filter(username=man,
                                               good=good)
        if len(valid_confirm) == 0:
            shop_car_to_save = ShopCar(username=man,
                                       good=good)
            shop_car_to_save.save()
    return HttpResponseRedirect(reverse('shop:my_car'))


def delete_from_car(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")

    good_in_car = ShopCar.objects.filter(username=man,
                                         good=good)
    if len(good_in_car) == 0:
        return render(request, "NOPage.html")
    else:
        good_in_car.delete()

    return HttpResponseRedirect(reverse('shop:my_car'))


def car_page(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    car = ShopCar.objects.filter(username=man)
    buy_authority = ""
    no_good = ""
    if len(car) == 0:
        buy_authority = "hidden"
        no_good = "无商品"

    return render(request, "ShopCar.html", {"car": car,
                                            "buy_authority": buy_authority,
                                            "no_good": no_good})


def car_increase_amount(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)[0]
    amount_to_change = ShopCar.objects.filter(username=man, good=good)[0]
    amount_to_change.good_amount += 1
    amount_to_change.save()
    return HttpResponseRedirect(reverse('shop:my_car'))


def car_reduce_amount(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)[0]
    amount_to_change = ShopCar.objects.filter(username=man, good=good)[0]
    if amount_to_change.good_amount > 1:
        amount_to_change.good_amount -= 1
        amount_to_change.save()
    return HttpResponseRedirect(reverse('shop:my_car'))


def buy(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    clean_not_pay_list()

    user = User.objects.get(name=man)

    goods_number = request.POST.getlist('checkbox_list')
    if len(goods_number) == 0:
        return HttpResponseRedirect(reverse('shop:my_car'))

    # 订单号的生成
    number_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    number_random = random.randint(0, 999999)
    number = str(number_time) + str(number_random).zfill(6)

    total_money = 0
    good_in_detail_list = []
    for one in goods_number:
        good = Goods.objects.filter(number=one)[0]
        if len(Goods.objects.filter(number=one)) == 0:
            continue
        in_car = ShopCar.objects.filter(username=user.name, good=good)[0]
        if len(ShopCar.objects.filter(username=user.name, good=good)) == 0:
            continue
        total_money = total_money + good.price*in_car.good_amount

        detail_list_to_save = DetailList(number=number,
                                         buyer=user,
                                         seller=good.seller.name,
                                         goods_number=good.number,
                                         goods_version=good.version,
                                         amount=in_car.good_amount)

        one_good = {"good": good, "amount": in_car.good_amount}
        good_in_detail_list.append(one_good)
        detail_list_to_save.save()
    return render(request, "DetailList.html", {"total_money": total_money,
                                               "good_in_detail_list": good_in_detail_list,
                                               "number": number})


def pay(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    clean_not_pay_list()

    list_number = request.POST.get('number')
    user = User.objects.get(name=man)

    detail_list = DetailList.objects.filter(buyer=user,
                                            number=list_number)
    total_money = 0
    if len(detail_list) == 0:
        return render(request, "NOPage.html", {})

    for one in detail_list:
        total_money += Goods.objects.filter(number=one.goods_number)[0].price * \
                       DetailList.objects.filter(buyer=user, goods_number=one.goods_number)[0].amount

    if user.fund < total_money:
        result = "余额不足"
        return HttpResponseRedirect(reverse('shop:welcome'))
    else:
        for one in detail_list:
            good = Goods.objects.filter(number=one.goods_number)
            good_in_car = ShopCar.objects.filter(username=user.name,
                                                 good=good)
            if one.amount > good[0].amount:
                result = "库存不足"
                return HttpResponseRedirect(reverse('shop:welcome'))

        for one in detail_list:
            good = Goods.objects.filter(number=one.goods_number)
            good_in_car = ShopCar.objects.filter(username=user.name,
                                                 good=good)

            one.status = 1
            one.save()
            good_in_car.delete()

        for one in detail_list:

            Goods.objects.filter(number=one.goods_number)[0].amount -= \
                        DetailList.objects.filter(buyer=user, goods_number=one.goods_number)[0].amount
            Goods.objects.filter(number=one.goods_number)[0].turnover += \
                DetailList.objects.filter(buyer=user, goods_number=one.goods_number)[0].amount

            Goods.objects.filter(number=one.goods_number)[0].save()

        user.fund -= total_money
        user.save()

    return HttpResponseRedirect(reverse('shop:buyer_list'))


def clean_not_pay_list():
    all_list = DetailList.objects.all()
    for one in all_list:
        if one.status == 0:
            if one.create_time.replace(tzinfo=None) + datetime.timedelta(hours=8, minutes=3) < \
                    datetime.datetime.now().replace(tzinfo=None):
                one.delete()


def show_buyer_list(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    user = User.objects.filter(name=man)

    detail_list = DetailList.objects.filter(buyer=user).order_by('status', '-create_time')

    all_list = []
    for one in detail_list:
        good = Goods.objects.filter(number=one.goods_number, version=one.goods_version)
        if len(good) == 0:
            good = OldGoods.objects.filter(number=one.goods_number, version=one.goods_version)
        if len(good) == 0:
            continue
        else:
            good = good[0]
            one_total = good.price * one.amount
            if one.status == 0:
                list_situation = "未付款"
            elif one.status == 1:
                list_situation = "未完成"
            elif one.status == 2:
                list_situation = "已完成"
            elif one.status == 3:
                list_situation = "已评论"
            else:
                list_situation = ""
            the_good = {"detail_list": one, "good": good, "one_total": one_total, "list_situation": list_situation}
            all_list.append(the_good)

    return render(request, "BuyerList.html", {"all_list": all_list})


def show_seller_list(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    seller = User.objects.filter(name=man)[0]

    detail_list = DetailList.objects.filter(seller=seller.name).order_by('status', '-create_time')

    all_list = []
    for one in detail_list:
        good = Goods.objects.filter(number=one.goods_number, version=one.goods_version)
        if len(good) == 0:
            good = OldGoods.objects.filter(number=one.goods_number, version=one.goods_version)
        if len(good) == 0:
            continue
        else:
            good = good[0]
            one_total = good.price * one.amount
            if one.status == 0:
                list_situation = "未付款"
            elif one.status == 1:
                list_situation = "未完成"
            elif one.status == 2:
                list_situation = "已完成"
            elif one.status == 3:
                list_situation = "买家已评论"
            else:
                list_situation = ""
            the_good = {"detail_list": one, "good": good, "one_total": one_total, "list_situation": list_situation}
            all_list.append(the_good)

    return render(request, "SellerList.html", {"all_list": all_list})


def finish_list(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    seller = User.objects.filter(name=man)

    list_number = request.POST.get('list_number')
    # good_number = request.POST.get('good_number')
    good_number = str(int(request.POST.get('good_number')))

    if len(list_number) == 0 or len(good_number) == 0:
        return render(request, "NOPage.html", {})
    buyer = DetailList.objects.filter(number=list_number,
                                      goods_number=good_number)[0].buyer

    if len(buyer.name) == 0:
        return render(request, "NOPage.html", {})

    the_list = DetailList.objects.filter(number=list_number,
                                         goods_number=good_number)

    if len(the_list) == 0:
        return render(request, "NOPage.html", {})

    if the_list[0].status != 1:
        return render(request, "NOPage.html", {})

    good = Goods.objects.filter(number=the_list[0].goods_number, version=the_list[0].goods_version)
    if good[0].amount < the_list[0].amount:
        result = "库存不足"
        return HttpResponseRedirect(reverse('shop:seller_list'))

    the_list[0].status = 2
    the_list[0].save()

    if len(good) == 0:
        return render(request, "NOPage.html", {})

    seller = seller[0]
    seller.fund = seller.fund + good[0].price * the_list[0].amount

    good[0].amount -= the_list[0].amount
    good[0].turnover += the_list[0].amount

    seller.save()
    good[0].save()
    return HttpResponseRedirect(reverse('shop:seller_list'))


def show_my_goods(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    seller = User.objects.filter(name=man)
    all_goods = Goods.objects.filter(seller=seller)
    goods = []
    for one in all_goods:

        on_authority = "hidden"
        off_authority = "hidden"

        if one.status == 0:
            situation = "未上架"
            on_authority = ""
        elif one.status == 1:
            situation = "上架"
            off_authority = ""
        else:
            return HttpResponseRedirect(reverse('shop:welcome'))
        the_good = {"good": one, "situation": situation,
                    "on_authority": on_authority,
                    "off_authority": off_authority}
        goods.append(the_good)
    return render(request, "MyGoods.html", {"goods": goods})


def put_on(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")

    good = good[0]

    if good.seller.name == man:
        if good.status == 0:
            good.put_on_time = datetime.datetime.now().replace(tzinfo=None)
            good.status = 1
            good.save()

    return HttpResponseRedirect(reverse('shop:my_goods'))


def put_off(request, number):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 2:
        return HttpResponseRedirect(reverse('shop:welcome'))

    good = Goods.objects.filter(number=number)
    if len(good) == 0:
        return render(request, "NOPage.html")

    good = good[0]

    if good.seller.name == man:
        if good.status == 1:
            good.status = 0
            good_in_car = ShopCar.objects.filter(good=good)
            if len(good_in_car) != 0:
                good_in_car.delete()
            good.save()

    return HttpResponseRedirect(reverse('shop:my_goods'))


def commit(request):

    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    list_number = request.POST.get("list_number")
    good_number = request.POST.get('good_number')

    user = User.objects.filter(name=man)[0]

    good_in_list = DetailList.objects.filter(buyer=user,
                                             goods_number=good_number,
                                             status=2)

    if len(good_in_list) == 0:
        return HttpResponseRedirect(reverse('shop:buyer_list'))

    good = Goods.objects.filter(number=good_number)[0]
    if request.method == "POST":
        form = CommentForm(request.POST)

        if not form.is_valid():
            result = "输入正确的验证码"
            return render(request, "CommitPage.html", {"form": form, "number": good_number,
                                                       "good": good, "result": result,
                                                       "list_number": list_number,
                                                       "good_number": good_number
                                                       })
        else:
            commit_content = form.cleaned_data['comment_content']
            if len(commit_content) == 0:
                return render(request, "CommitPage.html", {"form": form, "number": good_number, "good": good,
                                                           "list_number": list_number,
                                                           "good_number": good_number})
            else:
                commit_to_save = Comment(user=user,
                                         goods=good,
                                         content=commit_content)
                commit_to_save.save()
                good_in_list[0].status = 3
                good_in_list[0].save()
                return HttpResponseRedirect(reverse('shop:buyer_list'))

    else:
        form = CommentForm()
        return render(request, "CommitPage.html", {"form": form, "number": good_number, "good": good,
                                                   "list_number": list_number,
                                                   "good_number": good_number})


def turn_to_commit(request):
    man = check_cookie(request)

    if man is False:
        return HttpResponseRedirect(reverse('shop:welcome'))

    confirmation = User.objects.filter(name=man)
    if len(confirmation) == 0 or confirmation[0].type != 1:
        return HttpResponseRedirect(reverse('shop:welcome'))

    if request.method == "POST":
        list_number = request.POST.get('list_number')
        good_number = request.POST.get('good_number')
        form = CommentForm()

        user = User.objects.filter(name=man)[0]

        good_in_list = DetailList.objects.filter(buyer=user,
                                                 goods_number=good_number,
                                                 status=2)
        if len(good_in_list) == 0:
            return HttpResponseRedirect(reverse('shop:buyer_list'))

        good = Goods.objects.filter(number=good_number)[0]

        return render(request, "CommitPage.html", {"form": form,
                                                   "good": good,
                                                   "list_number": list_number,
                                                   "good_number": good_number})




