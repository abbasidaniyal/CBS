from django.contrib import admin
from django.utils.html import format_html

from projects.models import Client, Project, GalleryImage
from core.utils import ExportCsvMixin


class ClientAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["client_name", "client_website", "image_tag"]
    list_editable = ["client_website"]
    actions = ["export_as_csv"]

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.client_logo.url))

    image_tag.short_description = 'Logo'


class ProjectAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        "project_name",
        "client",
        "city",
        "architect",
        "year",
        "project_description",
        "expertise",
        "image_tag"
    ]
    list_editable = [
        "client",
        "city",
        "architect",
        "year",
        "project_description",
        "expertise",
    ]
    actions = ["export_as_csv"]

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.cover_image.image.url))

    image_tag.short_description = 'Cover image'


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(GalleryImage)
