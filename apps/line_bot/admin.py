from django.contrib import admin

from .models import (
    LineModel, LineAdmin,
    TheaterModel, TheaterAdmin,
    MovieModel,  MovieAdmin,
    ScheduleModel,ScheduleAdmin,
)
# Register your models here.

admin.site.register(LineModel , LineAdmin)
admin.site.register(TheaterModel , TheaterAdmin)
admin.site.register(MovieModel , MovieAdmin)
admin.site.register(ScheduleModel,ScheduleAdmin)
