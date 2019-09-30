from django.contrib import admin
from django.urls import re_path,path
from . import views

app_name = "web_site"
urlpatterns = [
    path('', views.home, name='web_site'),
    path('notebook/', views.notebook, name = 'web_notebook'),
    path('c1_movieline/', views.movieline, name = 'collection_movieline'),
    path('collection/<int:pk>/', views.collection, name = 'collection'),
    path('aboutme/', views.aboutme, name = 'web_aboutme'),
    path('omnifood/', views.omnifood, name = 'web_omnifood'),

]


