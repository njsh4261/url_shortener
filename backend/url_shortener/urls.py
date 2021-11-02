# from django.urls import path
from django.conf.urls import url
from django.urls import path

from . import views
from .constants import *

urlpatterns = [
    path("", views.index, name="index"),
    path(URL_ENC, views.get_encoded_url, name="get_encoded_url"),
    url(r"^(?P<shorten_url>[A-Za-z0-9]{1,8})$", views.get_decoded_url, name="get_decoded_url"),
]
