from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
# Create your models here.
class Country(models.Model):
    name = models.CharField(
        verbose_name=_('Country Name'),
        max_length=200,
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Country Slug')

    )

    def __str__(self):
        return self.name

#
class State(models.Model):
    name = models.CharField(
        verbose_name=_('State'),
        max_length=300,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_('Country')
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('State Slug')

    )
    def __str__(self):
        return self.name
#
class City(models.Model):
    name = models.CharField(
        verbose_name=_('City'),
        max_length=200,
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name=_('State'),
        blank=True,
        null=True
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('City Slug')

    )
    def __str__(self):
        return self.name
class Area(models.Model):
    name = models.CharField(
        verbose_name=_('Area Name'),
        max_length=350,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_('City')
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Area Slug')

    )

    def __str__(self):
        return self.name