from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.
from Util.utils import rand_slug


class Slider(models.Model):
    image = models.ImageField(
        verbose_name=_('Slider Image'),
        upload_to='slider_images'
    )
    link = models.URLField(
        blank=True,null=True,
        verbose_name=_('Image Link')
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Slider Slug')

    )


