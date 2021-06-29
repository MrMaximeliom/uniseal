from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Brochures(models.Model):
    title = models.CharField(
        max_length=120,
        verbose_name=_('Document Title')
    )
    attachment = models.FileField(
        verbose_name=_('Document Attachment'),
        upload_to='document_field'
    )
