from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug


# Create your models here.

class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=150
    )
    arabic_name = models.CharField(
        max_length=120,
        verbose_name=_('Category Name (Arabic)'),
        null=True,
        blank=True
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Product Slug')

    )
    def get_absolute_url(self):
        return reverse_lazy("allCategories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = str(self.name) + '' + str(rand_slug())
        self.slug = slugify(value)
        super().save(*args, **kwargs)

