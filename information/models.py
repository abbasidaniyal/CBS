from django.db import models


class HomePageInformation(models.Model):
    tag_line = models.CharField("Tagline ", max_length=100,)
    brief_description = models.CharField(
        "Small Introduction", max_length=2000,)

    about_card_1_title = models.CharField("About Us 1 Title", max_length=50)
    about_card_1_description = models.CharField(
        "About Us 1 Description", max_length=200)
    about_card_1_image = models.ImageField(
        "About Us 1 Image ", upload_to="homepage", )

    about_card_2_title = models.CharField("About Us 2 Title", max_length=50)
    about_card_2_description = models.CharField(
        "About Us 2 Description", max_length=200)
    about_card_2_image = models.ImageField(
        "About Us 2 Image ", upload_to="homepage", )

    about_card_3_title = models.CharField("About Us 3 Title", max_length=50)
    about_card_3_description = models.CharField(
        "About Us 3 Description", max_length=200)
    about_card_3_image = models.ImageField(
        "About Us 3 Image ", upload_to="homepage", )

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(HomePageInformation, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class FactCounter(models.Model):

    def __str__(self):
        return self.count_title

    count_title = models.CharField("Count Title", max_length=10, default="", )
    count_value = models.IntegerField(("Count Value"), default=0)
    home_page = models.ForeignKey(
        HomePageInformation,  on_delete=models.CASCADE)


class AboutUsInfo(models.Model):
    main_description_paragraph_1 = models.TextField(
        "First About Us Paragraph ", max_length=500)
    main_description_paragraph_2 = models.TextField(
        "Second About Us Paragraph ", max_length=500)
    main_description_paragraph_3 = models.TextField(
        "Third About Us Paragraph ", max_length=1000)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(AboutUsInfo, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class WhyUsCard(models.Model):

    class Meta:
        ordering = ('id', )

    card_header = models.CharField(("Why Us Card Header"), max_length=15)
    card_body = models.CharField(("Why Us Card Body"), max_length=250)

    card = models.ForeignKey(AboutUsInfo, verbose_name=("Why Us"),
                             on_delete=models.CASCADE, default=None)


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
    organisation = models.CharField(max_length=50,)
    contact_number = models.CharField(max_length=13)
    query = models.TextField("Comments")
    query_date = models.DateTimeField(auto_now_add=True)


class Staff(models.Model):
    staff_name = models.CharField("Name", max_length=50)
    staff_designation = models.CharField("Designation", max_length=50)
    staff_about = models.CharField("About Staff", max_length=250, default="")
    staff_picture = models.ImageField("Photo ", upload_to="staff",)

    def __str__(self):
        return self.staff_name
