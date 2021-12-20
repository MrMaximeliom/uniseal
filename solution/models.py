from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Solution(models.Model):
    title = models.CharField(
        verbose_name=_('Solution Title'),
        max_length=150
    )
    arabic_title = models.CharField(
        verbose_name=_('Solution Title(Arabic)'),
        max_length=150,
        null=True
    )
    description = models.TextField(
        verbose_name=_('Solution Description'),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class SolutionImages(models.Model):
    image = models.ImageField(
        upload_to="solution_images",
        verbose_name=_('Solution Image')
    )
    solution = models.ForeignKey(
        Solution,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Solution')
    )


class SolutionVideos(models.Model):
    video = models.URLField(
        verbose_name=_('Solution Video Url')
    )
    solution = models.ForeignKey(
        Solution,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Solution')
    )


