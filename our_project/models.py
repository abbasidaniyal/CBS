from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
    project_description = models.CharField(
        "Project Description", max_length=300, default="NONE")


class Service(models.Model):
    def __str__(self):
        return self.name_of_service + " ("+str(self.pk)+")"

    title_image = models.ImageField(
        "Service Heading", upload_to="services", default="default.jpg", null=True)
    name_of_service = models.CharField("Name of Service", max_length=50,)


class Products(models.Model):

    def __str__(self):
        return self.name_of_product + " ("+str(self.pk)+")"

    title_image = models.ImageField(
        "Product", upload_to="products", default="default.jpg", null=True)
    name_of_product = models.CharField("Name of Product", max_length=50,)


class ProjectManagementConsultantAndMaintainence(models.Model):
    def __str__(self):
        return self.pmc_for + " ("+str(self.pk)+")"

    title_image = models.ImageField(
        "Service Heading", upload_to="services", default="default.jpg", null=True)
    pmc_for = models.CharField("PMC for ", max_length=50,)


class MyGalleryImage(models.Model):
    image = models.ImageField("Image", upload_to="gallery")
    image_description = models.CharField(
        "Image Description", max_length=50, blank=True)

    limits = models.Q(app_label='our_project', model='products') | models.Q(app_label='our_project', model='service') | models.Q(
        app_label='our_project', model='projectmanagementconsultantandmaintainence')
    content_type = models.ForeignKey(ContentType, related_name="Image_Type+",
                                     null=True, on_delete=models.SET_NULL, limit_choices_to=limits)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id',)
    project = models.ForeignKey(Project, verbose_name=(
        "Project"), on_delete=models.SET_NULL,null=True)
