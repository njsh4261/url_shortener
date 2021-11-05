from django.conf.urls import url
from django.urls import path

from . import views
from .src.constants import URL_ENC

app_name = "url_shortener"
urlpatterns = [
    path("", views.index, name="index"),
    path(URL_ENC, views.post_encode_url, name="get_encoded_url"),
    url(r"^(?P<shorten_url>[A-Za-z0-9]{1,8})$", views.get_decode_url, name="get_decoded_url"),
]
