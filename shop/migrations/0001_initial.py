# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-02 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('key', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DetailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('seller', models.CharField(max_length=20)),
                ('goods_number', models.CharField(max_length=20)),
                ('goods_version', models.IntegerField()),
                ('amount', models.IntegerField(default=1)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('finish_time', models.DateTimeField(null=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('version', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('amount', models.IntegerField()),
                ('turnover', models.IntegerField(default=0)),
                ('image', models.CharField(max_length=100)),
                ('description', tinymce.models.HTMLField()),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('put_on_time', models.DateTimeField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OldGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('version', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('image', models.CharField(max_length=100)),
                ('description', tinymce.models.HTMLField()),
                ('create_time', models.DateTimeField()),
                ('put_on_time', models.DateTimeField()),
                ('put_off_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ShopCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('good_amount', models.IntegerField(default=1)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=80)),
                ('answer', models.CharField(max_length=80)),
                ('fund', models.FloatField(default=0)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='oldgoods',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='goods',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='detaillist',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Goods'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
    ]
