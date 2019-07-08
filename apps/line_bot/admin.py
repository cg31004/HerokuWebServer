from django.contrib import admin
from .models import LineModel,TheaterModel,MovieModel
# Register your models here.

admin.site.register(LineModel)
admin.site.register(TheaterModel)
admin.site.register(MovieModel)
