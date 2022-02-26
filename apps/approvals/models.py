from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from Util.utils import rand_slug

"""
Approval Model:
this model is used to save approvals
details
"""
class Approval(models.Model):
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Approval Slug'),
        unique=True

    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=300
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        upload_to="approvals_images",
    )
    file = models.FileField(
        upload_to='brochures_document',
        verbose_name=_("File"),
        null=True,
        blank=True

    )
