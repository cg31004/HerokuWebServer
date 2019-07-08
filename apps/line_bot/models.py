from django.db import models
from django.conf import settings 
from django.contrib import admin
# Create your models here.

class LineModel(models.Model):
    line_id = models.CharField(max_length=66, verbose_name='lineID',primary_key=True)
    line_token = models.CharField(max_length=200, blank=True, verbose_name='line通行代碼')


    def __str__(self):
        return str(self.line_id)

    class Meta:
        db_table = 'line'
        verbose_name = 'line使用者'
        verbose_name_plural = 'line使用者'
    
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def change_view(self, request, object_id, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)




class TheaterModel(models.Model):
    theater_id = models.CharField(max_length=66, verbose_name='TheaterID',primary_key=True)
    theater_name = models.CharField(max_length=66, verbose_name='TheaterName')

    def __str__(self):
        return str(self.theater_id)
    
    class Meta:
        db_table = 'theater'
        verbose_name = 'Theater清單'
        verbose_name_plural = 'Theater清單'

    # def has_add_permission(self, request, obj=None):
    #     return False
    # def change_view(self, request, object_id, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)





class MovieModel(models.Model):
    movie_id = models.CharField(max_length=66, verbose_name='MovieID',primary_key=True)
    movie_name = models.CharField(max_length=66, verbose_name='MovieName')

    def __str__(self):
        return str(self.movie_id)
    
    class Meta:
        db_table = 'movie'
        verbose_name = 'Movie清單'
        verbose_name_plural = 'Movie清單'

    # def has_add_permission(self, request, obj=None):
    #     return False
    # def change_view(self, request, object_id, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     return super(SessionAdmin, self).change_view(request, object_id, extra_context=extra_context)

    



