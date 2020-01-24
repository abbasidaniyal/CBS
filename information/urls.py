from django.conf.urls import url,include
from django.urls import path
from information import views
from our_project import views as service_views


urlpatterns = [
    path('', views.HomePageView,name='home'),
    path('about-us/' ,views.AboutUsViewSet,name='about_us'),
    path('contact-us/' ,views.ContactUsPageView,name='contact_page'),
    path('gallery/' ,views.GalleryPageView,name='gallery'),
    path('expertise/' ,views.ExpertisePageView,name='expertise'),
    path('gallery-service/<int:pk>' , service_views.ServicePageView ,name='gallery-service'),
    # path('temp/' , views.temp ,name='temp'),


]