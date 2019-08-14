from django.conf.urls import url,include
from django.urls import path
from information import views


urlpatterns = [
    path('', views.HomePageView,name='home'),
    path('about-us/' ,views.AboutUsViewSet,name='about_us'),
    path('contact-us/' ,views.ContactUsPageView,name='contact_page'),
    path('gallery/' ,views.GalleryPageView,name='gallery'),

]