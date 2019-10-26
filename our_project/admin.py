from django.contrib import admin

from .models import Client,Project,MyGalleryImage,ProvidedService

# Register your models here.
admin.site.register(ProvidedService)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(MyGalleryImage)