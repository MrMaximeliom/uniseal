from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify # new
import string
import random
def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

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

