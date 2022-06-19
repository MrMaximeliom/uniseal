from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Create your models here.
from Util.utils import rand_slug


class SellingPoint(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_('Sale Point Name')
    )
    arabic_name = models.CharField(
        max_length=150,
        verbose_name=_('Sale Point Name(Arabic)'),
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='sale_point_image',
        verbose_name=('Sale Point Image')
    )
    location = models.CharField(
        max_length=200,
        verbose_name=_('Sale Point Location')
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_('Sale Point Address')
    )
    country = models.ForeignKey(
        'address.Country',
        on_delete=models.SET_NULL,

        blank=True,
        null=True
    )
    state = models.ForeignKey(
        'address.State',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

    )
    city = models.ForeignKey(
        'address.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

    )
    area = models.ForeignKey(
        'address.Area',
        on_delete=models.SET_NULL,
        null=True,
        blank = True,

    )
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )
    secondary_phone = models.CharField(
        max_length=20,
        verbose_name=_('Sale Point Secondary Phone'),
        default=""

    )
    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        unique=True,

    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Selling Point Slug')

    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + "-" + str(datetime.now().second))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("allSellingPoints")
        # return not wanted fields' names in the process of creating new report file from this model

    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug","arabic_name",
                "image","location","address"]




