from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def redirect(request, shorten_url):
    return HttpResponse("URL requests will be redirected by this view.")

def index(request):
    return HttpResponse("Hey there!")
