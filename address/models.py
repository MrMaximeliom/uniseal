from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Country(models.Model):
    name = models.CharField(
        verbose_name=_('Country Name'),
        max_length=200,
    )
class City(models.Model):
    name = models.CharField(
        verbose_name=_('City Name'),
        max_length=200,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_('Country')
    )
