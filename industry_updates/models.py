from django.db import models
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
from django.template.defaultfilters import slugify


# Create your models here.
class IndustryUpdates(models.Model):
    headline = models.CharField(
        max_length=200,
        verbose_name=_('Title'),
        blank = True,
        null=True
    )
    link = models.URLField(
        verbose_name=_('Link'),

    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Industry Slug')

    )
