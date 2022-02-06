from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from Util.utils import rand_slug

class JopType(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        blank=False,
        null=False,
        max_length=150
    )

    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Job Type Slug')
    )


    def __str__(self):
        return self.name