from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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

        null=True,
        blank=True

    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=300
    )
    file = models.FileField(
        upload_to='approvals_document',
        verbose_name=_("File"),
        null=True,
        blank=True

    )
    def save(self, *args, **kwargs):
        from datetime import datetime
        self.slug = slugify(rand_slug() + "-" + str(self.name) + "-"+str(datetime.now().second))
        return super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse_lazy("approvalsList")
    def __str__(self):
        return self.name


"""
Approval Image Model:
this model is used to save approvals' images
details
"""
class ApprovalImage(models.Model):
    image = models.ImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        upload_to="approvals_images",
    )
    approval = models.ForeignKey(
        Approval,
        verbose_name=_("Approval"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="approval_images"
    )
    def get_absolute_url(self):
        return reverse_lazy("approvalImages-dash")



