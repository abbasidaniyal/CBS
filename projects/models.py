from django.contrib.contenttypes.models import ContentType
from django.db import models


class Client(models.Model):
    def __str__(self):
        return self.client_name

    client_name = models.CharField("Client's Name", max_length=50)
    client_logo = models.ImageField("Client's Logo", upload_to="clients")


class Project(models.Model):
    def __str__(self):
        return self.project_name

    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    project_name = models.CharField("Project Name", max_length=50)
    project_address = models.CharField("Site Address", max_length=50)
    project_description = models.CharField(
        "Project Description", max_length=300, default="NONE")


class GalleryImage(models.Model):
    def __str__(self):
        return self.image_description + " @ " + self.project.project_name

    image = models.ImageField("Image", upload_to="gallery")
    image_description = models.CharField(
        "Image Description", max_length=50, blank=True)
    project = models.ForeignKey(Project, verbose_name=("Project"), on_delete=models.DO_NOTHING, null=True)
