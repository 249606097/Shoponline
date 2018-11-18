from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r'^welcome', views.jump_to_welcome_page, name='welcome'),

    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
]
