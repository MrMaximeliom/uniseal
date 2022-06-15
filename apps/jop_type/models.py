from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.name))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("jobTypesList")