from django.urls import path

from projects.views import GalleryPageView

urlpatterns = [
    path( 'gallery/', GalleryPageView, name='gallery' ),
]
