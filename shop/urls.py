from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^static/img/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^welcome', views.jump_to_welcome_page, name='welcome'),

    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),

    # url(r'^edit', views.edit, name='edit'),

    url(r'^add', views.add, name='add'),
    url(r'^list', views.goods_list, name='list'),
    url(r'^good/(?P<number>\d+)$', views.good_page, name='good_page'),
    url(r'^delete_good/(?P<number>\d+)/$', views.delete_good, name="delete_good"),

    # url(r'^add/$', views.add),
    # url(r'do_add/$', views.do_add),

    url(r'^edit', views.edit_good, name='edit'),
    url(r're_edit/(?P<number>\d+)', views.re_edit, name='re_edit'),

    url(r'^index', views.edit_good, name='index'),
    url(r'upload/$', views.upload, name='upload_img'),
    # url(r'^static/img/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^create_good', views.create_good, name="create_good"),


    url(r'$', views.jump_to_none),
]

