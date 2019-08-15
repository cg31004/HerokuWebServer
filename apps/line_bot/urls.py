"""Django_root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from . import views


# Default API setting
from rest_framework.routers import DefaultRouter
from apps.line_bot.views import RankViewSet,ControllerViewSet


# router = routers.SimpleRouter()
router = DefaultRouter()

router.register(r'rank', RankViewSet,base_name='rank')
router.register(r'controller', ControllerViewSet,base_name='controller')
# router.register(r'theater', TheaterViewSet)


# rank_list = RankViewSet.as_view({'get': 'list'})
# rank_id = RankViewSet.as_view({'get': 'same_id'})

urlpatterns = [
    path('callback/', views.callback, name='line_bot'),
    path('iwantdeleteschedule/', views.deleteAll, name='line_bot'),  

    # path('api/', include(router.urls)), 
    # path('api/<slug:slug>/',views.api_list, name='api'), 
    # path('api/<slug:slug>/<int:order>/',views.api_single, name='api'),
]

#append api url
urlpatterns+=router.urls