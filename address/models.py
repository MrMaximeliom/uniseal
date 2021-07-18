from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Country(models.Model):
    name = models.CharField(
        verbose_name=_('Country Name'),
        max_length=200,
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

    def __str__(self):
        return self.name