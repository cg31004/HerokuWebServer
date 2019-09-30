from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
from ratelimit.decorators import ratelimit

# Create your views here.


def home(request):
    return render(request,'home.html',locals())



def notebook(request):
    object_tag = '<object type="text/html" data="https://simonsu.postach.io/" width = 100% height = 100% style="float:left;" ></object>'
    return HttpResponse(object_tag)

def movieline(request):
    return render(request,'movieline.html',locals())

def collection(request,pk):
    if pk == 1:
        return render(request,'movieline.html',locals())

def aboutme(request):
    return render(request,'aboutme.html',locals())

def omnifood(reqiest):
    return render(reqiest, 'omnifood.html', locals())




