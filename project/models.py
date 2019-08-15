from django.db import models

# Create your models here.



class Client(models.Model):
    client_name = models.CharField("Client's Name", max_length=50)
    client_logo = models.ImageField("Client's Logo", upload_to="clients")


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_name = models.CharField("Project Name", max_length=50)
    project_location = models.CharField("Site Address", max_length=50)


class GalleryImage(models.Model):
    image = models.ImageField("Image", upload_to="gallery")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
