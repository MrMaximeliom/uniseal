from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
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

    def get_absolute_url(self):
        return reverse_lazy("allCountries")

    def save(self, *args, **kwargs):
        value = str(self.name) + '' + str(rand_slug())
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    # return not wanted fields' names in the process of creating new report file from this model
    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug"]


#
class State(models.Model):
    name = models.CharField(
        verbose_name=_('State'),
        max_length=300,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Country'),
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('State Slug')

    )

    def __str__(self):
        return str(self.name)

    # return not wanted fields' names in the process of creating new report file from this model
    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug"]

    def get_absolute_url(self):
        return reverse_lazy("allStates")

    def save(self, *args, **kwargs):
        value = str(self.name) + '' + str(rand_slug())
        self.slug = slugify(value)
        super().save(*args, **kwargs)


#
class City(models.Model):
    name = models.CharField(
        verbose_name=_('City'),
        max_length=200,
    )

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('State'),
        blank=True,

    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('City Slug')

    )

    def save(self, *args, **kwargs):
        value = str(self.name) + '' + str(rand_slug())
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("allCities")

    # return not wanted fields' names in the process of creating new report file from this model
    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug"]


class Area(models.Model):
    name = models.CharField(
        verbose_name=_('Area Name'),
        max_length=350,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('City')
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Area Slug')

    )

    def save(self, *args, **kwargs):
        value = str(self.name) + '' + str(rand_slug())
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("allAreas")

    # return not wanted fields' names in the process of creating new report file from this model
    def get_not_wanted_fields_names_in_report_file(self=None):
        return ["id", "slug"]
