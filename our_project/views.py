from django.shortcuts import render

from information.models import Carousel 
from our_project.models import GalleryImage

def ServicePageView(request,pk):
    context = {
        'carousel': Carousel.objects.all(),
        'images': GalleryImage.objects.filter(service=pk)

    }
    return render(request,'our_project/service_page.html',context)

    



