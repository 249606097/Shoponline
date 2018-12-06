from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=80)
    answer = models.CharField(max_length=80)
    fund = models.FloatField(default=0)
    type = models.IntegerField()

    def __str__(self):
        return self.name


class Goods(models.Model):
    number = models.CharField(max_length=20)
    version = models.IntegerField()
    seller = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    amount = models.IntegerField()
    turnover = models.IntegerField(default=0)
    image = models.CharField(max_length=100)
    description = HTMLField()
    create_time = models.DateTimeField(default=timezone.now)
    put_on_time = models.DateTimeField()
    status = models.IntegerField(default=0)
    # status 0 为 未上架
    #        1 为 上架

    def __str__(self):
        return self.name


class OldGoods(models.Model):
    number = models.CharField(max_length=20)
    version = models.IntegerField()
    seller = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.CharField(max_length=100)
    description = HTMLField()
    create_time = models.DateTimeField()
    put_on_time = models.DateTimeField()
    put_off_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class DetailList(models.Model):
    number = models.CharField(max_length=20)
    buyer = models.ForeignKey(User)
    seller = models.CharField(max_length=20)
    goods_number = models.CharField(max_length=20)
    goods_version = models.IntegerField()
    amount = models.IntegerField(default=1)
    create_time = models.DateTimeField(default=timezone.now)
    finish_time = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    # status 0为订单 创建 未付款
    #        1为订单 付款 未完成
    #        2为订单 完成 可评论
    #        3为订单  已评论


class Comment(models.Model):
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    time = models.DateTimeField(default=timezone.now)
    content = HTMLField()  # 富文本


class ShopCar(models.Model):
    username = models.CharField(max_length=20)
    good = models.ForeignKey(Goods)
    good_amount = models.IntegerField(default=1)


class Cookie(models.Model):
    user_name = models.CharField(max_length=20)
    key = models.CharField(max_length=30)
    create_time = models.DateTimeField(default=timezone.now)


