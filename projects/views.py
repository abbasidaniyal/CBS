from django.shortcuts import render
from django.views.generic import ListView, DetailView

from projects.models import GalleryImage, Project, Client


class ProjectListView(ListView):
    model = Project


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["image_list"] = GalleryImage.objects.filter(project=self.get_object())
        return context


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context["image_list"] = GalleryImage.objects.filter(
            project=Project.objects.filter(client=self.get_object())
        )
        context["project_list"] = Project.objects.filter(client=self.get_object())
        return context


def GalleryPageView(request):
    context = {"gallery_page": "active", "images": GalleryImage.objects.all()}
    return render(request, "projects/gallery.html", context)
