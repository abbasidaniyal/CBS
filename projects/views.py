from django.shortcuts import render

from projects.models import GalleryImage



def GalleryPageView(request):
    context = {
        'gallery_page': "active",
        'images': GalleryImage.objects.all()
    }
    return render( request, 'information/gallery.html', context )


def ServicePageView(request,pk):
    context = {
        'images': GalleryImage.objects.filter(service=pk)

    }
    return render(request,'our_project/service_page.html',context)

    



