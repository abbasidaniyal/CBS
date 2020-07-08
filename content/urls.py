from django.urls import path

from content.views import QueryPageView, HomePageView


urlpatterns = [
    path("", HomePageView, name="home"),
    path("contact-us/", QueryPageView.as_view(), name="contact_page"),
]
