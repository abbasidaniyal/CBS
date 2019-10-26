from django.db import models



class ProvidedService(models.Model):
    def __str__(self):
        return self.name_of_service
    
    title_image = models.ImageField("Service Heading", upload_to="services",default="default.jpg",null=True)
    name_of_service = models.CharField("Name of Service", max_length=50,)


class Client(models.Model):
    def __str__(self):
        return self.client_name

    client_name = models.CharField("Client's Name", max_length=50)
    client_logo = models.ImageField("Client's Logo", upload_to="clients")





class Project(models.Model):
    def __str__(self):
        return self.project_name

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_name = models.CharField("Project Name", max_length=50)
    project_location = models.CharField("Site Address", max_length=50)
    project_description = models.CharField("Project Description", max_length=300,default="NONE")



class MyGalleryImage(models.Model):
    image = models.ImageField("Image", upload_to="gallery")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(ProvidedService,on_delete=models.CASCADE)