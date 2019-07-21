from django.contrib import admin

from .models import (
    TheaterModel, TheaterAdmin,
    MovieModel,  MovieAdmin,
    ScheduleModel,ScheduleAdmin,
    ControllerModel,ControllerAdmin,
    RankModel,RankAdmin,
)
# Register your models here.


admin.site.register(TheaterModel , TheaterAdmin)
admin.site.register(MovieModel , MovieAdmin)
admin.site.register(ScheduleModel,ScheduleAdmin)
admin.site.register(ControllerModel,ControllerAdmin)
admin.site.register(RankModel,RankAdmin)

