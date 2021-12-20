from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug


# Create your models here.
class Brochures(models.Model):
    title = models.CharField(
        max_length=120,
        verbose_name=_('Document Title')
    )
    arabic_title = models.CharField(
        max_length=120,
        verbose_name=_('Document Title (Arabic)'),
        null=True,
        blank=True
    )
    attachment = models.FileField(
        verbose_name=_('Document Attachment'),
        upload_to='brochures_document'
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Brochure Slug')

    )

