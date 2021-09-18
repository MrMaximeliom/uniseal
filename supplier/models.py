from django.db import models
from django.template.defaultfilters import slugify  # new
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug


class Supplier(models.Model):
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Supplier Slug')

    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Supplier Name')
    )
    image = models.ImageField(
        verbose_name=_('Supplier Image'),
        upload_to= 'supplier_images/',
    )
    link = models.URLField(
        verbose_name=_('Link'),
        default=''
    )

    def __str__(self):
        return self.name

