from django.contrib import admin
# from .forms import ImageTypeForm


from .models import Client,Project,MyGalleryImage,Service,Products,ProjectManagementConsultantAndMaintainence



@admin.register(MyGalleryImage)
class ImageAdmin(admin.ModelAdmin):
    # form=ImageTypeForm
    pass


# Register your models here.
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Products)
admin.site.register(ProjectManagementConsultantAndMaintainence)
# admin.site.register(MyGalleryImage)