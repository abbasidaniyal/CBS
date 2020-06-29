from django.db import models

class Carousel(models.Model):
    class Meta:
        verbose_name = 'Slide Show Image'
        verbose_name_plural = 'Slide Show Images'

    image_carousel = models.ImageField(upload_to="carousel")
    title = models.CharField(max_length=20)
    detail = models.CharField(max_length=80)


class ContactUs(models.Model):
    name = models.CharField(max_length=50, )
    email = models.EmailField()
    organisation = models.CharField(max_length=50, blank=True)
    contact_number = models.CharField(max_length=13)
    query = models.TextField("Comments")
    query_date = models.DateTimeField(auto_now_add=True)


class Staff(models.Model):
    staff_name = models.CharField("Name", max_length=50)
    staff_designation = models.CharField("Designation", max_length=50)
    staff_about = models.CharField("About Staff", max_length=250, default="")
    staff_picture = models.ImageField("Photo ", upload_to="staff", )

    def __str__(self):
        return self.staff_name
