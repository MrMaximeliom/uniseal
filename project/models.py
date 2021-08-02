from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify # new
import string
import random
from Util.utils import max_value_current_year,current_year
from django.core.validators import MinValueValidator
import datetime


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
# Create your models here.

def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]
class Application(models.Model):
    name = models.CharField(
        verbose_name=_('Project Application'),
        max_length=300
    )
    def __str__(self):
        return self.name
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
    beneficiary_description = models.TextField(
        verbose_name=_('Beneficiary Description'),
        null=True,
        blank=True
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Project Slug')

    )
    # execution_date = models.DateField(
    #     verbose_name=_('Project Execution Date'),
    #
    # )
    application = models.ForeignKey(
       Application,
        verbose_name=_('Application'),
        on_delete=models.SET_NULL,
        null=True
    )
    execution_year = models.IntegerField(
        _('Execution Year'),
        validators=[MinValueValidator(2000), max_value_current_year],
        default=2020,



    )



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.title))
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.name + str(self.category)

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

