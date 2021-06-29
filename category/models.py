from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=150
    )

