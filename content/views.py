from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, resolve_url
from django.views.generic import CreateView

from content.forms import QueryForm
from content.models import Query
from projects.models import Client, GalleryImage


def HomePageView(request):
    context = {
        "home_page": "active",
        "clients": Client.objects.all(),
    }
    return render(request, "information/index.html", context)


class QueryPageView(SuccessMessageMixin, CreateView):
    model = Query
    form_class = QueryForm
    template_name = "information/contact-us.html"
    success_message = "Thank you. We will get back to you shortly!"
    success_url = "/contact-us"

    def get_context_data(self, **kwargs):
        context = super(QueryPageView, self).get_context_data(**kwargs)
        context["contact_page"] = "active"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail(
            "New Query from Website",
            f"""
{form.data.get( "name" )}
{form.data.get( "email" )}
{form.data.get( "organisation" )}
{form.data.get( "contact_number" )}
{form.data.get( "query" )}               
                   """,
            form.data.get("email"),
            [settings.EMAIL_HOST_USER],
            fail_silently=True
        )

        return response
