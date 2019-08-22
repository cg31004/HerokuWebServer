from django.db import models
from django.conf import settings 
from django.contrib import admin
from django.contrib.sessions.models import Session
from rest_framework import serializers
# Create your models here.


##############     User Controller     ################
class ControllerModel(models.Model):
    mod_choice = [(0,None),(1,'rank'),(2,'keyword')]

    line_id =  models.CharField(max_length=66, primary_key=True, verbose_name='用戶')
    mod = models.IntegerField( verbose_name = 'Mod',null=True)
    movie_id = models.CharField(max_length=66, verbose_name = 'MovieID',null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name = '選取時間',null=True)
    control = models.CharField(max_length=100, verbose_name='控制器',null=True)

    def __str__(self):
        return str(self.line_id)

    class Meta:
        app_label ='line_bot'
        db_table = 'line.Controller'
        verbose_name = 'Line 互動訊息'
        verbose_name_plural = 'Line 互動訊息'
    
    

class ControllerAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(ControllerAdmin, self).change_view(request, object_id, extra_context=extra_context)

#######  api
class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControllerModel
        # fields = '__all__'
        fields = ("line_id",)

##############     Theater     ################
class TheaterModel(models.Model):
    theater_name = models.CharField(max_length=66, verbose_name='TheaterName')
    theater_area =  models.CharField(max_length=66, verbose_name='TheaterArea')
    theater_address =  models.CharField(max_length=66, verbose_name='TheaterAddress')
    
    def __str__(self):
        return str(self.theater_id)
    class Meta:
        app_label ='line_bot'
        db_table = 'line.theater'
        verbose_name = 'Theater清單'
        verbose_name_plural = 'Theater清單'


class TheaterAdmin(admin.ModelAdmin):
    actions = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(TheaterAdmin, self).change_view(request, object_id, extra_context=extra_context)

#######  api
class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterModel
        # fields = '__all__'
        fields = ("theater_name","theater_area","theater_address",)

##############     Movie     ################
class MovieModel(models.Model):
    movie_id = models.CharField(max_length=66, verbose_name='MovieID',primary_key=True)
    movie_name = models.CharField(max_length=66, verbose_name='MovieName')

    def __str__(self):
        return str(self.movie_id)
    
    class Meta:
        app_label ='line_bot'
        db_table = 'line.movie'
        verbose_name = 'Movie清單'
        verbose_name_plural = 'Movie清單'


class MovieAdmin(admin.ModelAdmin):
    actions = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(MovieAdmin, self).change_view(request, object_id, extra_context=extra_context)
#######  api
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = '__all__'
        # fields = ("theater_name","theater_area","theater_address",)



##############     Schedule     ################
class ScheduleModel(models.Model):
    movie_date = models.DateField(auto_now=False, auto_now_add=False)
    movie_id = models.CharField(max_length=66, verbose_name='Sch_MovieID')
    area = models.CharField(max_length=66, verbose_name='ScheduleArea')
    theater_id = models.CharField(max_length=66, verbose_name='Sch_theaterID')
    movie_type = models.CharField(max_length=66, verbose_name='ScheduleType')
    movie_time = models.TimeField(("%H:%M"), auto_now=False, auto_now_add=False)

    

    def __str__(self):
        return str(self.id)
    
    class Meta:
        app_label ='line_bot'
        db_table = 'line.schedule'
        verbose_name = 'schedule清單'
        verbose_name_plural = 'schedule清單'


class ScheduleAdmin(admin.ModelAdmin):
    actions = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(ScheduleAdmin, self).change_view(request, object_id, extra_context=extra_context)


##############     Rank     ################
class RankModel(models.Model):
    rank_date = models.DateField(auto_now=False, auto_now_add=False)
    rank = models.IntegerField(verbose_name='Rank')
    movie_id = models.CharField(max_length=66, verbose_name='MovieID')
    movie_name = models.CharField(max_length=66, verbose_name='MovieName')
    

    def __str__(self):
        return str(self.id)
    
    class Meta:
        app_label ='line_bot'
        db_table = 'line.rank'
        verbose_name = 'rank 列表'
        verbose_name_plural = 'rank 列表'


class RankAdmin(admin.ModelAdmin):
    actions = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(RankAdmin, self).change_view(request, object_id, extra_context=extra_context)

##### api

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankModel
        fields = '__all__'
        # fields = ("rank_date","rank",'movie_name')
        
    
    



    



