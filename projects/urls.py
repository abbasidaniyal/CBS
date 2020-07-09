from django.urls import path

from projects.views import (
    GalleryPageView,
    ProjectListView,
    ProjectDetailView,
    ClientListView,
    ClientDetailView,
)

urlpatterns = [
    path("gallery/", GalleryPageView, name="gallery"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("project/<slug:slug>", ProjectDetailView.as_view(), name="project-detail"),
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("client/<slug:slug>", ClientDetailView.as_view(), name="client-detail"),
]
