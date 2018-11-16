from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    user_answer = models.CharField(max_length=8)
    user_fund = models.FloatField
    user_type = models.IntegerField()


class Goods(models.Model):
    goods_id = models.IntegerField
    goods_version = models.IntegerField
    goods_name = models.CharField(max_length=200)
    goods_price = models.FloatField
    goods_amount = models.IntegerField
    goods_turnover = models.IntegerField
    goods_image = models.ImageField
    goods_description = models.CharField(max_length=10000)
    goods_create_time = models.DateTimeField(default=timezone.now)
    goods_put_on_time = models.DateTimeField()
    goods_status = models.IntegerField


class DetailList(models.Model):
    list_id = models.IntegerField
    list_buyer = models.CharField(max_length=20)
    list_seller = models.ForeignKey(User)
    list_goods_id = models.IntegerField
    list_goods_version = models.IntegerField
    list_create_time = models.DateTimeField(default=timezone.now)
    list_finish_time = models.DateTimeField
    list_status = models.IntegerField


class Comment(models.Model):
    comment_user = models.ForeignKey(User)
    comment_goods = models.ForeignKey(Goods)
    comment_time = models.DateTimeField(default=timezone.now)
    comment_content = models.CharField(max_length=500)
    comment_image = models.ImageField


class ShopCar(models.Model):
    car_user = models.ForeignKey(User)
    car_the_goods_id = models.IntegerField
    car_the_goods_version = models.IntegerField
    car_the_goods_amount = models.IntegerField


class Cookie(models.Model):
    cookie_user_name = models.CharField(max_length=20)
    cookie_key = models.CharField(max_length=10)
    cookie_create_time = models.DateTimeField(default=timezone.now)


