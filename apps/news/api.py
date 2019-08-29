from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import MultipleObjectsReturned

from apps.news.models import NewsModel,NewsSerializer
from apps.news.models import ContentModel,ContentSerializer

class NewsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = NewsModel.objects.all().order_by('-news_id')
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)

class ContentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = ContentModel.objects.all()
        serializer = ContentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def id(self, request,pk):
        content_id = int(pk)
        queryset = ContentModel.objects.all()
        queryset = get_object_or_404(queryset,content_id=content_id)
        serializer = ContentSerializer(queryset)
        return Response(serializer.data)