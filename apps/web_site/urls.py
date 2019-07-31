from django.contrib import admin
from django.urls import re_path,path
from . import views

app_name = "web_site"
urlpatterns = [
    path('', views.home, name='web_site'),
    path('info/',views.info,name = 'web_info'),
    path('notebook/',views.notebook,name = 'web_notebook'),
    path('test/',views.limit_test,name = 'test')
]
