from django import template
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import ShortenURL
from .src.constants import *
from .src.base62 import encode_base62, decode_base62

# Create your views here.
def index(request): # encode_url
    template = loader.get_template('url_shortener/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    # return HttpResponse("This is an index page.")

@csrf_exempt
def get_encoded_url(request):
    if request.method != "POST":
        return HttpResponseForbidden()

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
            + encode_base62(url_record.id)
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
    if request.method != "GET":
        return HttpResponseForbidden()
    return redirect(
        get_object_or_404(ShortenURL, pk=decode_base62(shorten_url)).url
    )
