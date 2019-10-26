from django.shortcuts import render

from information.models import Carousel 
from our_project.models import ProvidedService,MyGalleryImage

# Create your views here.

def ServicePageView(request,pk):
    context = {
        "service": ProvidedService.objects.get(pk=pk),
        'carousel': Carousel.objects.all(),
        'images': MyGalleryImage.objects.filter(service=pk)

    }
    return render(request,'our_project/service_page.html',context)

    



