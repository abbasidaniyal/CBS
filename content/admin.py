import csv

from django.contrib import admin

from content.models import ContactUs, Staff

from core.utils import ExportCsvMixin


class ContactUsAdmin( admin.ModelAdmin, ExportCsvMixin ):
    list_display = ['name', 'email', 'contact_number', 'query', 'query_date']
    actions = ["export_as_csv"]


admin.site.register( ContactUs, ContactUsAdmin )
admin.site.register( Staff )
