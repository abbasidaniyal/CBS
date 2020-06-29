from django.shortcuts import render

from content.models import Carousel
from projects.models import GalleryImage

def ServicePageView(request,pk):
    context = {
        'carousel': Carousel.objects.all(),
        'images': GalleryImage.objects.filter(service=pk)

    }
    return render(request,'our_project/service_page.html',context)

    


