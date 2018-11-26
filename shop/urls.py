from django.conf.urls import url
from shop import views


from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.static import serve
from django.conf import settings

print(settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^welcome', views.jump_to_welcome_page, name='welcome'),

    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^edit', views.edit, name='edit'),
    url(r'^add', views.add, name='add'),
    url(r'^list', views.goods_list, name='list'),



    # url(r'^add/$', views.add),
    # url(r'do_add/$', views.do_add)

    url(r'^index', views.index, name='index'),
    url(r'upload/$', views.upload, name='upload_img'),
    url(r'^static/img/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^create_good', views.create_good, name="create_good"),
]
