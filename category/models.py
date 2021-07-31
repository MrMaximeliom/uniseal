from django.db import models
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=150
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Product Slug')

    )

    def __str__(self):
        return self.name

