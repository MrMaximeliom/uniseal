from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Create your models here.
from Util.utils import rand_slug


class Slider(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=200,
        blank=True,
        null=True
    )
    arabic_title = models.CharField(
        verbose_name=_("Title(Arabic)"),
        max_length=200,
        blank=True,
        null=True
    )
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
    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + "-" + str(datetime.now().second))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("allSliders")


