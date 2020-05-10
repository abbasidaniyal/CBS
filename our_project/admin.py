from django.contrib import admin
# from .forms import ImageTypeForm


from .models import Client,Project,GalleryImage




admin.site.register(Client)
admin.site.register(Project)
admin.site.register(GalleryImage)