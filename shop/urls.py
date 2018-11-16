from django.conf.urls import url, include
from shop import views

urlpatterns = [
    url(r'^register', views.register, name='register'),

]
