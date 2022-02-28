from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from Util.utils import rand_slug
from django.template.defaultfilters import slugify


class Offer(models.Model):
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to="offer_images",
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active Offer?'),
        blank=False,
        default=False,
    )
    offer_created_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    offer_start_date = models.DateField(blank=True, null=True)
    offer_end_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Offer Slug'),
        null=True,
        blank=True
    )
    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + str(self.name) + "-"+str(datetime.now().second))
        return super().save(*args, **kwargs)

