from django.shortcuts import render
from django.views.generic import ListView, DetailView

from projects.models import GalleryImage, Project, Client


class ProjectListView(ListView):
    model = Project
    ordering = ["project_name"]


class ProjectDetailView(DetailView):
    model = Project
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["image_list"] = GalleryImage.objects.filter(project=self.get_object())
        return context


class ClientListView(ListView):
    model = Client
    ordering = ["client_name"]


class ClientDetailView(DetailView):
    model = Client
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context["image_list"] = GalleryImage.objects.filter(
            project__in=Project.objects.filter(client=self.get_object())
        )
        context["project_list"] = Project.objects.filter(client=self.get_object())
        return context


def GalleryPageView(request):
    context = {"gallery_page": "active", "images": GalleryImage.objects.all()}
    return render(request, "projects/gallery.html", context)
