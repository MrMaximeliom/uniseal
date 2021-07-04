from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Project(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Project Name')
    )
    title = models.CharField(
        max_length=120,
        verbose_name=_('Project Title')
    )
    category = models.CharField(
        max_length=100,
        verbose_name=_('Project Category')
    )
    beneficiary = models.CharField(
        max_length=100,
        verbose_name=_('Project Beneficiary')
    )
    image = models.ImageField(
        upload_to='project_images',
        verbose_name=_('Project Image')
    )
    description = models.TextField(
        verbose_name=_('Project Description'),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class ProjectImages(models.Model):
    image = models.ImageField(
        upload_to="project_images",
        verbose_name=_('Project Image')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )


class ProjectVideos(models.Model):
    video = models.URLField(
        verbose_name=_('Project Video Url')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )

class ProjectSolutions(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project Solution'),
        on_delete=models.CASCADE,
    )
    solution = models.ForeignKey(
        "solution.Solution",
        verbose_name=_('Project Solution'),
        on_delete=models.CASCADE,
    )