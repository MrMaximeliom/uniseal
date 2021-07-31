from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.
from Util.utils import rand_slug


class SellingPoint(models.Model):
    from Util.ListsOfData import CITIES_CHOICES, AREA_CHOICES
    name = models.CharField(
        max_length=150,
        verbose_name=_('Sale Point Name')
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
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    state = models.ForeignKey(
        'address.State',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        'address.City',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    area = models.ForeignKey(
        'address.Area',
        on_delete=models.CASCADE,
        blank = True,
        null = True
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

