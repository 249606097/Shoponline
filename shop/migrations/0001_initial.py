# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-17 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_content', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie_user_name', models.CharField(max_length=20)),
                ('cookie_key', models.CharField(max_length=10)),
                ('cookie_create_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DetailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_buyer', models.CharField(max_length=20)),
                ('list_create_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=200)),
                ('goods_description', models.CharField(max_length=10000)),
                ('goods_create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('goods_put_on_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ShopCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_password', models.CharField(max_length=80)),
                ('user_answer', models.CharField(max_length=80)),
                ('user_fund', models.FloatField(default=0)),
                ('user_type', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='shopcar',
            name='car_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='detaillist',
            name='list_seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Goods'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
    ]
