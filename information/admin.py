from django.contrib import admin

from information.models import Carousel, ContactUs, Staff


# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact_number', 'query', 'query_date']




admin.site.register(Carousel)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Staff)
