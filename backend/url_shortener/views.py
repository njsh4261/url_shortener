from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import ShortenURL
from .src.constants import URL_ENC
from .src.base62 import encode_base62, decode_base62

def index(request): # encode_url
    """ [GET /] """
    if request.method != "GET":
        return HttpResponseForbidden()
    return HttpResponse(
        loader.get_template('url_shortener/index.html')
            .render( {}, request )
    )

@csrf_exempt
def post_encode_url(request):
    """ [POST /enc-url] """
    if request.method != "POST":
        return HttpResponseForbidden()

    response_data = {
        "shorten_url": None,
        "message": None
    }
    status_code = 200

    try:
        # request body should include URL like { "url": "https://www.github.com" }
        print(request.POST)
        url_fetched = request.POST.get("url")
        if not url_fetched.endswith("/"):
            url_fetched += "/"

        # add 'https://' or 'http://' if url does not start with them
        url_record = None
        if url_fetched.startswith("https://") or url_fetched.startswith("http://"):
            url_record = ShortenURL.objects.filter(url=url_fetched)
        else:
            url_record = ShortenURL.objects.filter(url="https://" + url_fetched)
            if not url_record:
                url_record = ShortenURL.objects.filter(url="http://" + url_fetched)

        # if the url dose not exist in the table, insert new record
        if not url_record:
            url_record = ShortenURL(url=url_fetched)
            url_record.save()
        else:
            url_record = url_record[0]

        # response 200 ok
        response_data["shorten_url"] = request.build_absolute_uri()[:-len(URL_ENC)] \
            + encode_base62(url_record.id)
        response_data["message"] = "Success! You may copy the shorten URL above."

    except ValidationError as e:
        # URL is not in vaild form
        if "url" in e.message_dict:
            response_data["message"] = "The URL may be invalid. Try something else."
            status_code = 400
        else:
            response_data["message"] = "Sorry. There is a problem with the service."
            status_code = 500

    response = JsonResponse(response_data)
    response.status_code = status_code
    return response

def get_decode_url(request, shorten_url):
    """ [GET /[url_shorten]] """
    if request.method != "GET":
        return HttpResponseForbidden()
    return redirect(
        get_object_or_404(ShortenURL, pk=decode_base62(shorten_url)).url
    )
