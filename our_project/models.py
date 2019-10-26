from django.db import models




class Client(models.Model):
    client_name = models.CharField("Client's Name", max_length=50)
    client_logo = models.ImageField("Client's Logo", upload_to="clients")


class Service(models.Model):
    name_of_service = models.CharField("Name of Service", max_length=50)





class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)
    project_name = models.CharField("Project Name", max_length=50)
    project_location = models.CharField("Site Address", max_length=50)
    project_description = models.CharField("Project Description", max_length=300,default="NONE")



class GalleryImage(models.Model):
    image = models.ImageField("Image", upload_to="gallery")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
