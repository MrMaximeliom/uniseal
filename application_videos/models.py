from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ProductApplicationVideos(models.Model):
    application_video = models.URLField(
        verbose_name=_('Product Video Url'))
    project = models.ForeignKey(
        "project.Project",
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )