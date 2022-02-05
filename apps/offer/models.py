from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Offer(models.Model):
    image = models.ImageField(
        verbose_name=_('Image'),
        blank=False,
        null=False
    )
    offer_created_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    offer_start_date = models.DateField(blank=True, null=True)
    offer_end_date = models.DateField(blank=True, null=True)