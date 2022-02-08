from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class RequestAccess(models.Model):
    status = models.BooleanField(
        verbose_name=_("Access Status"),

    )
    user = models.ForeignKey(
          "accounts.User",
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        blank=False

    )