from django.contrib import admin
from .models import top10alltime
from import_export.admin import ImportExportModelAdmin

class MovieAdmin(ImportExportModelAdmin):
    list_display=['title','runtime']

admin.site.register(top10alltime, MovieAdmin)