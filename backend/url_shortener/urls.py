# from django.urls import path
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^(?P<shorten_url>[A-Za-z0-9]{1,8})$', views.redirect, name=''),
]
