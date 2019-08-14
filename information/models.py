from django.db import models
# from stdimage import StdImageField


class HomePage(models.Model):
    tag_line = models.CharField(max_length=100, default="")
    brief_description = models.CharField(max_length=2000, default="")

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(HomePage, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class AboutUsInfo(models.Model):
    main_description = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(AboutUsInfo, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class Carousel(models.Model):
    image_carousel = models.ImageField(upload_to="carousel")
    title = models.CharField(max_length=20)
    detail = models.CharField(max_length=80)


class ContactUs(models.Model):

    name = models.CharField(max_length=50, )
    email = models.EmailField()
    contact_number = models.CharField(max_length=13)
    query = models.CharField(max_length=500)
    query_date = models.DateTimeField(auto_now_add=True)
