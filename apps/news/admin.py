from django.contrib import admin

# Register your models here.
from .models import (
     NewsModel, NewsAdmin,
    ContentModel,  ContentAdmin,
)

admin.site.register(NewsModel , NewsAdmin)
admin.site.register(ContentModel , ContentAdmin)