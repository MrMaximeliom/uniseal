from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug


# Create your models here.
class IndustryUpdates(models.Model):
    headline = models.CharField(
        max_length=200,
        verbose_name=_('Title'),
        blank = True,
        null=True
    )
    arabic_headline = models.CharField(
        max_length=200,
        verbose_name=_('Title(Arabic)'),
        blank = True,
        null=True
    )
    link = models.CharField(
        verbose_name=_('Source'),
        default="Uniseal Construction Chemicals Co Ltd",
        max_length=400
    )
    image_link = models.URLField(
        verbose_name=_('Image Link'),

    )
    details = models.TextField(
        verbose_name=_('Details')
    )
    arabic_details = models.TextField(
        verbose_name=_('Details(Arabic)'),
        null=True,
        blank=True
    )

    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Industry Slug')

    )
    date = models.DateField(
        verbose_name=_('Date'),

    )
