from django.conf.urls import url, include
from shop import views

urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^welcome', views.turn_to_welcome_page, name='welcome')
]
