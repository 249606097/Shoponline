from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^static/img/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^welcome', views.welcome, name='welcome'),

    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^forget_password$', views.forget_password, name='forget_password'),
    url(r'^logout$', views.logout, name='logout'),

    # url(r'^edit', views.edit, name='edit'),

    # url(r'^add', views.add, name='add'),

    url(r'^list$', views.goods_list, name='list'),
    url(r'^good/(?P<number>\d+)$', views.good_page, name='good_page'),
    url(r'^delete_good/(?P<number>\d+)/$', views.delete_good, name='delete_good'),

    # url(r'^add/$', views.add),
    # url(r'do_add/$', views.do_add),

    url(r'^edit$', views.edit_good, name='edit'),
    url(r're_edit/(?P<number>\d+)/$', views.re_edit, name='re_edit'),

    url(r'upload/$', views.upload, name='upload_img'),
    # url(r'^static/img/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^create_good$', views.create_good, name='create_good'),

    url(r'^add_to_car/(?P<number>\d+)/$', views.add_to_car, name='add_to_car'),
    url(r'^delete_from_car/(?P<number>\d+)/$', views.delete_from_car, name='delete_from_car'),
    url(r'^my_car$', views.car_page, name='my_car'),
    url(r'^car_increase_amount/(?P<number>\d+)/$', views.car_increase_amount, name='car_increase_amount'),
    url(r'^car_reduce_amount/(?P<number>\d+)/$', views.car_reduce_amount, name='car_reduce_amount'),

    url(r'^buy$', views.buy, name='buy'),
    url(r'^pay$', views.pay, name='pay'),

    url(r'^buyer$', views.show_buyer_list, name='buyer_list'),
    url(r'^seller$', views.show_seller_list, name='seller_list'),

    url(r'^finish_list', views.finish_list, name='finish_list'),
    url(r'^my_goods$', views.show_my_goods, name='my_goods'),
    url(r'^put_on/(?P<number>\d+)/$', views.put_on, name='put_on'),
    url(r'^put_off/(?P<number>\d+)/$', views.put_off, name='put_off'),
    url(r'^to_commit$', views.turn_to_commit, name='turn_to_commit'),
    url(r'^commit$', views.commit, name='commit'),
    url(r'^search$', views.search, name='search'),

    url(r'$', views.jump_to_none),
]

