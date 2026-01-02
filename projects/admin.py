from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html
from django.contrib import messages

from projects.models import Client, Project, GalleryImage
from projects.forms import BulkImportForm
from core.utils import ExportCsvMixin, BulkImportProcessor


class ClientAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["client_name", "client_website", "image_tag"]
    list_editable = []  # Made read-only
    actions = ["export_as_csv"]

    def image_tag(self, obj):
        if obj.client_logo:
            return format_html('<img src="{}" style="max-height: 50px;" />'.format(obj.client_logo.url))
        return "-"

    image_tag.short_description = 'Logo'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


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
    list_editable = []  # Made read-only
    actions = ["export_as_csv"]

    def image_tag(self, obj):
        if obj.cover_image and obj.cover_image.image:
            return format_html('<img src="{}" style="max-height: 50px;" />'.format(obj.cover_image.image.url))
        return "-"

    image_tag.short_description = 'Cover image'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["image_description", "project", "image_tag"]
    list_filter = ["project"]
    search_fields = ["image_description", "project__project_name"]
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />'.format(obj.image.url))
        return "-"
    
    image_tag.short_description = 'Image'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


def bulk_import_view(request):
    """Custom admin view for bulk import"""
    if request.method == 'POST':
        form = BulkImportForm(request.POST, request.FILES)
        if form.is_valid():
            zip_file = request.FILES['zip_file']
            
            # Process the import
            processor = BulkImportProcessor(zip_file)
            success, stats, errors = processor.process()
            
            # Display results
            if success:
                messages.success(
                    request,
                    f"Import completed successfully! "
                    f"Clients: {stats['clients_created']} created, {stats['clients_updated']} updated. "
                    f"Projects: {stats['projects_created']} created, {stats['projects_updated']} updated. "
                    f"Gallery Images: {stats['gallery_images_created']} created, {stats['gallery_images_updated']} updated."
                )
            else:
                messages.warning(
                    request,
                    f"Import completed with errors. "
                    f"Clients: {stats['clients_created']} created, {stats['clients_updated']} updated. "
                    f"Projects: {stats['projects_created']} created, {stats['projects_updated']} updated. "
                    f"Gallery Images: {stats['gallery_images_created']} created, {stats['gallery_images_updated']} updated."
                )
            
            # Display errors
            for error in errors:
                messages.error(request, error)
            
            return redirect('/admin/bulk-import/')
    else:
        form = BulkImportForm()
    
    context = {
        'form': form,
        'title': 'Bulk Import from Zip',
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
        'has_permission': True,
    }
    
    return render(request, 'admin/bulk_import.html', context)


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
