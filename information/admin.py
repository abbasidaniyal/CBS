from django.contrib import admin

from .models import HomePage,AboutUsInfo,Carousel,ContactUs
# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
      list_display    = ['name','email','contact_number','query','query_date']

admin.site.register(HomePage)
admin.site.register(AboutUsInfo)
admin.site.register(Carousel)
admin.site.register(ContactUs,ContactUsAdmin)

