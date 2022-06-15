from django.db import models
from django.template.defaultfilters import slugify  # new
from django.urls import reverse_lazy
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
    arabic_name = models.CharField(
        max_length=100,
        verbose_name=_('Supplier Name(Arabic)'),
        null=True,
        blank=True
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

    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + "-" + str(datetime.now().second))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("allSuppliers")

