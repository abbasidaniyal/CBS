import csv

from django.contrib import admin

from content.models import Query, Staff

from core.utils import ExportCsvMixin


class QueryAdmin( admin.ModelAdmin, ExportCsvMixin ):
    list_display = ['name', 'email', 'contact_number', 'query', 'query_date']
    actions = ["export_as_csv"]


admin.site.register( Query, QueryAdmin )
admin.site.register( Staff )
