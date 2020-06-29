from django.urls import path

from content.views import ContactUsPageView, HomePageView


urlpatterns = [
    path( '', HomePageView, name='home' ),
    path( 'contact-us/', ContactUsPageView.as_view(), name='contact_page' ),
]
