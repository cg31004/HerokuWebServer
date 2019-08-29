from django.contrib import admin
from django.urls import path,re_path,include
from .views import news
from rest_framework.routers import DefaultRouter
from apps.news.api import NewsViewSet,ContentViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet,base_name='news')
router.register(r'content', ContentViewSet,base_name='content')

urlpatterns = [
    path('', news, name='nba_news'),
]

#append api url
urlpatterns+=router.urls
