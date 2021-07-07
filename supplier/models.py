from django.db import models
from django.utils.translation import gettext_lazy as _

class Supplier(models.Model):
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

