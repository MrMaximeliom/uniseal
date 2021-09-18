from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug


# Create your models here.
class TokenIDs(models.Model):
    reg_id = models.CharField(
        verbose_name=_('Device Token'),
        max_length=800
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Token Slug')

    )
    os_type = models.CharField(
        verbose_name=_('OS Type'),
        max_length=150
    )

    def __str__(self):
        return self.reg_id

class Notifications(models.Model):
    token_id = models.ForeignKey(
        TokenIDs,
        verbose_name=_("Token ID"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(
        verbose_name=_("Notification Title"),
        max_length=250,
    )
    body = models.CharField(
        verbose_name=("Notification Body"),
        max_length=400
    )
    notification_date = models.DateField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    notification_time = models.TimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('Notification Slug')

    )


    def __str__(self):
        return self.token_id.reg_id