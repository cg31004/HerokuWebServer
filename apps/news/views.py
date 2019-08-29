from django.shortcuts import render
from apps.news.models import NewsModel
from django.http import HttpResponse

# Create your views here.


def news(request):
    return render(request,'news.html',locals())
    