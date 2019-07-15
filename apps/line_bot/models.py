from django.db import models
from django.conf import settings 
from django.contrib import admin
# Create your models here.

##############     Line     ################
class LineModel(models.Model):
    line_id = models.CharField(max_length=66, verbose_name='lineID',primary_key=True)
    line_token = models.CharField(max_length=200, blank=True, verbose_name='line通行代碼')


    def __str__(self):
        return str(self.line_id)

    class Meta:
        app_label ='line_bot'
        db_table = 'line.line'
        verbose_name = 'line使用者'
        verbose_name_plural = 'line使用者'
    
    

class LineAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request, obj=None):
        return False
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['can_change'] = False
        return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)



##############     Theater     ################
class TheaterModel(models.Model):
    theater_id = models.CharField(max_length=66, verbose_name='TheaterID',primary_key=True)
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
        return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)


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
        return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)



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
        return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)



    



