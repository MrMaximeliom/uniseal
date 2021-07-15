from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(
        verbose_name=_('Slider Image'),
        upload_to='slider_images'
    )
    link = models.URLField(
        blank=True,null=True,
        verbose_name=_('Image Link')
    )
