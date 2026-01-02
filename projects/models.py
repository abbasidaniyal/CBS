from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug


class Client(models.Model):
    """
    Client Model to store name, website and logo
    """

    def __str__(self):
        return self.client_name

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.client_name
            self.slug = generate_unique_slug(Client, value)
        super().save(*args, **kwargs)

    client_name = models.CharField("Client's Name", max_length=100)
    client_logo = models.ImageField("Client's Logo", upload_to="client_logos")
    client_website = models.URLField("Client's Website", blank=True)
    slug = models.SlugField(editable=False, unique=False)


class Project(models.Model):
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

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.project_name
            self.slug = generate_unique_slug(Project, value)
        super().save(*args, **kwargs)

    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, blank=True)
    project_name = models.CharField("Project Name", max_length=100)
    city = models.CharField("Site Location", max_length=200)
    project_description = models.TextField("Project Description", max_length=300,)
    architect = models.CharField("Architect", max_length=50, blank=True) # Can be a FK in future
    expertise = MultiSelectField(choices=EXPERTISE, default=EXPERTISE,)
    year = models.IntegerField("Year Completed")
    cover_image = models.ForeignKey(
        "GalleryImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="project_cover_image",
    )
    slug = models.SlugField(editable=False, unique=True)


class GalleryImage(models.Model):
    """
    Gallery Images linked to corresponding projects
    """

    def __str__(self):
        if self.project:
            desc = self.image_description or "Image"
            return f"{desc} @ {self.project.project_name}, {self.project.city}"
        return self.image_description or "Gallery Image"

    image = models.ImageField("Image", upload_to="gallery")
    image_description = models.CharField("Image Description", max_length=50, blank=True)
    project = models.ForeignKey(
        Project, verbose_name=("Project"), on_delete=models.DO_NOTHING, null=True
    )
