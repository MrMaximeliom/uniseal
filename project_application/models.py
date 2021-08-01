from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Application(models.Model):
    name = models.CharField(
        verbose_name=_('Project Application'),
        max_length=300
    )
    def __str__(self):
        return self.name