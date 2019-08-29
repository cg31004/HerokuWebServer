from django.db import models
from django.conf import settings 
from django.contrib import admin
from rest_framework import serializers

# Create your models here.
##############     News    ################
class NewsModel(models.Model):
    news_id = models.IntegerField(primary_key=True, verbose_name='newsid')
    # title =  models.TextField(max_length=66,verbose_name='title')
    # introduction = models.TextField(verbose_name='introduction')
    title =  models.TextField(max_length=66,verbose_name='title')
    introduction = models.TextField(verbose_name='introduction')
    

    def __str__(self):
        return str(self.news_id)+"--"+str(self.title)

    class Meta:
        app_label ='news'
        db_table = 'news.News'
        verbose_name = 'NBA新聞清單'
        verbose_name_plural = 'NBA 新聞清單'

class NewsAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(NewsAdmin, self).change_view(request, object_id, extra_context=extra_context)
#######  api
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'
    



##############     News    ################
class ContentModel(models.Model):
    content = models.OneToOneField(NewsModel, primary_key=True, related_name='content_id', on_delete=models.CASCADE, verbose_name='news_id')
    content_title =  models.TextField(max_length=66, verbose_name='title')
    content_url = models.TextField(max_length=180, verbose_name='url')
    content_text = models.TextField(verbose_name='text')
    news_date = models.DateTimeField(auto_now = False)

    class Meta:
        app_label ='news'
        db_table = 'news.content'
        verbose_name = 'NBA新聞內文'
        verbose_name_plural = 'NBA 新聞內文'

    def __str__(self):
        return str(self.content)+"--"+str(self.content_title)

class ContentAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(ContentAdmin, self).change_view(request, object_id, extra_context=extra_context)
#######  api
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModel
        fields = '__all__'


