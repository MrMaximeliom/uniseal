from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug

# Create your models here.
class WorkingField(models.Model):
    field_name = models.CharField(
        verbose_name=_('Working Field'),
        max_length=300
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Working Field Slug')

    )