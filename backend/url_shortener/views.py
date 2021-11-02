from django.core.exceptions import ValidationError
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, get_object_or_404

from .models import ShortenURL
from .constants import *

def _encode_base62(id):
    div_list = []
    while id > 0:
        div_list.append(id % BASE62)
        id //= BASE62
    return "".join([BASE62_TABLE[i] for i in div_list[::-1]])

def _decode_base62(shorten_url):
    try:
        base62_list = [BASE62_TABLE.index(c) for c in shorten_url]
        id = 0
        for i in base62_list:
            id = id * BASE62 + i
        return id
    except ValueError:
        return -1       # 404 error will be raised for a bad URL

# Create your views here.
def index(request): # encode_url
    return HttpResponse("This is an index page.")

def get_encoded_url(request):
    # if request.method != "POST":
    #     return HttpResponseForbidden()

    response_data = {
        "shorten_url": None,
        "message": None
    }
    status_code = 200

    try:
        # request body should include URL like { "url": "https://www.github.com" }
        url_fetched = request.POST.get("url")
        url_record = ShortenURL.objects.filter(url=url_fetched)
        if not url_record:
            url_record = ShortenURL(url=url_fetched)
            url_record.save()
        else:
            url_record = url_record[0]
        response_data["shorten_url"] = request.build_absolute_uri()[:-len(URL_ENC)] \
            + _encode_base62(url_record.id)
        response_data["message"] = "Successfully shortened the URL length!"
    except ValidationError as e:
        if "url" in e.message_dict: # URL is not in vaild form
            response_data["message"] = "The URL may be invalid. Try something else."
            status_code = 400
        else:
            response_data["message"] = "Sorry. There is a problem with the service."
            status_code = 500

    response = JsonResponse(response_data)
    response.status_code = status_code
    return response
    # return HttpResponse("In this page({0}) url will be encoded.".format(request.build_absolute_uri()[:-len(URL_ENC)]))

def get_decoded_url(request, shorten_url):
    return redirect(
        get_object_or_404(ShortenURL, pk=_decode_base62(shorten_url)).url
    )
