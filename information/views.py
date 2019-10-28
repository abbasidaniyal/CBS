from rest_framework import viewsets
from information.serializers import AboutUsSerializers
from information.models import AboutUsInfo, Carousel, HomePageInformation, ContactUs, Staff
from our_project.models import ProvidedService, Client
from django.shortcuts import render
from information.forms import ContactForm
from django.http import HttpResponseRedirect
import datetime
from django.core.mail import send_mail
from django.conf import settings


def HomePageView(request):
    context = {
        'home_page': "active",
        'home_page_fields': HomePageInformation.objects.get(),
        'carousel': Carousel.objects.all(),
        'clients': Client.objects.all(),
    }
    return render(request, 'information/index.html', context)


def AboutUsViewSet(request):

    info = AboutUsInfo.objects.get()
    context = {
        'about_info': info,
        'about_page': "active",
        'staff_list': Staff.objects.all(),
        'carousel': Carousel.objects.all(),
    }
    # print(dir(info.whyuscard_set.values))
    return render(request, 'information/about-us.html', context)


def GalleryPageView(request):

    context = {
        'gallery_page': "active",
        'carousel': Carousel.objects.all(),
        'services': ProvidedService.objects.all()
    }

    return render(request, 'information/gallery_page.html', context)


def ContactUsPageView(request):
    message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            query = form.save(commit=False)
            query.query_date = datetime.datetime.now()
            query.save()
            message = "Thank you. We will get back to you shortly!"
            send_mail("New Query from Website", query.query, query.email, [
                      'abbasi.daniyal98@gmail.com'], fail_silently=False)
            form = ContactForm()
        else:
            form = ContactForm(request.POST)

    else:
        form = ContactForm()

    context = {
        # 'about_info': info,
        'message': message,
        'form': form,
        'contact_page': "active",
        'carousel': Carousel.objects.all(),
    }
    return render(request, 'information/contact-us.html', context)
