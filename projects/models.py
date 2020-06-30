from django.contrib.contenttypes.models import ContentType
from django.db import models

from multiselectfield import MultiSelectField


class Client( models.Model ):
    """
    Client Model to store name, website and logo
    """

    def __str__(self):
        return self.client_name

    client_name = models.CharField( "Client's Name", max_length=100 )
    client_logo = models.ImageField( "Client's Logo", upload_to="client_logos" )
    client_website = models.URLField( "Client's Website", blank=True )


class Project( models.Model ):
    """
    Project models to record various projects done 
    """

    EXPERTISE = [
        ("SS", "Steel Structures"),
        ("TMS", "Tensile Membrane Structures"),
        ("RF", "Roofings"),
        ("CD", "Claddings"),
        ("SS", "Services"),
        ("SC", "Studio Connect"),
    ]

    def __str__(self):
        return self.project_name

    client = models.ForeignKey( Client, on_delete=models.DO_NOTHING, blank=True )
    project_name = models.CharField( "Project Name", max_length=100 )
    city = models.CharField( "Site Location", max_length=200 )
    project_description = models.TextField( "Project Description", max_length=300, )
    architect = models.CharField( "Architect", max_length=50, blank=True )
    expertise = MultiSelectField( choices=EXPERTISE, default=EXPERTISE )
    year = models.IntegerField( "Year Completed" )


class GalleryImage( models.Model ):
    """
    Gallery Images linked to corrusponding projects
    """

    def __str__(self):
        return self.image_description + " @ " + self.project.project_name + ", " + self.project.city

    image = models.ImageField( "Image", upload_to="gallery" )
    image_description = models.CharField(
        "Image Description", max_length=50, blank=True )
    project = models.ForeignKey( Project, verbose_name=("Project"), on_delete=models.DO_NOTHING, null=True )
