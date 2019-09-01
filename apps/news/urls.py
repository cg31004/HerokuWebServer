from django.contrib import admin
from django.urls import path,re_path,include
from .views import news, news1
from rest_framework.routers import DefaultRouter
from apps.news.api import NewsViewSet,ContentViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet,base_name='news')
router.register(r'content', ContentViewSet,base_name='content')

urlpatterns = [
    path('', news, name='nba_news'),
    path('1/', news1, name='nba_news2'),
]

#append api url
urlpatterns+=router.urls
