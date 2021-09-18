import datetime
import random
import string

from django.db import models
from django.template.defaultfilters import slugify  # new
from django.utils.translation import gettext_lazy as _


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
# Create your models here.

def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]
class Application(models.Model):
    name = models.CharField(
        verbose_name=_('Project Type'),
        max_length=300
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Project Type Slug')

    )
    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Project Name')
    )

    beneficiary = models.CharField(
        max_length=100,
        verbose_name=_('Project Beneficiary'),
        null=True,
        blank=True
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

    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Project Slug')

    )
    main_material = models.CharField(
        verbose_name=_('Main Material Used'),
        # will remove later to make it required field as it supposed to be
        null=True,
        blank=True,
        max_length=350

    )
    project_type = models.ForeignKey(
       Application,
        verbose_name=_('Project Type'),
        on_delete=models.SET_NULL,
        null=True
    )


    date = models.CharField(
        _('Project Date'),
        max_length=100,

    )
    rank = models.IntegerField(
        verbose_name=_('Project Order'),

    )



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.name))
        return super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name) + "-" + str(self.main_material)

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
    is_default = models.BooleanField(
        verbose_name=_('Default Image?'),
        default=False
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

