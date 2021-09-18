from django.db import models
from django.template.defaultfilters import slugify  # new
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug
# Create your models here.
class ProductApplicationVideos(models.Model):
    application_video = models.URLField(
        verbose_name=_('Product Video Url'))
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        verbose_name=_('Product')
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Product Video Slug')

    )
