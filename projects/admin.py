from django.contrib import admin

from projects.models import Client, Project, GalleryImage
from core.utils import ExportCsvMixin


class ClientAdmin( admin.ModelAdmin, ExportCsvMixin ):
    list_display = ['client_name', 'client_website', 'client_logo']
    actions = ["export_as_csv"]


class ProjectAdmin( admin.ModelAdmin, ExportCsvMixin ):
    list_display = ['project_name', 'client', 'city', 'architect', 'year', 'project_description', 'expertise']
    actions = ["export_as_csv"]


admin.site.register( Client, ClientAdmin )
admin.site.register( Project, ProjectAdmin )
admin.site.register( GalleryImage )
