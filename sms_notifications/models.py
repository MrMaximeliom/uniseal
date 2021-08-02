from django.db import models
from django.utils.translation import gettext_lazy as _



class SMSGroups(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Group Name')
    )
    group_created_datetime = models.DateTimeField(
        verbose_name=_('Group Created DateTime'),
        auto_now=True, blank=True, null=True
    )

class SMSNotification(models.Model):
    sender = models.CharField(
        max_length=11,
        verbose_name=_('SMS Sender')
    )
    message = models.TextField(
        verbose_name=_('SMS Message'),

    )
    group = models.ForeignKey(
        'SMSGroups',
        on_delete=models.SET_NULL,
        verbose_name=_('SMS Group'),
        blank=True,
        null=True
    )
    single_mobile_number = models.CharField(
        verbose_name=_('Single Mobile Number'),
        max_length=20,
        blank=True,
        null=True
    )
    is_multiple = models.BooleanField(
        verbose_name=('Is Message Sent To Many Users?')

    )

class SMSContacts(models.Model):
    contact_number = models.CharField(
        max_length=18,
        verbose_name=_('Contact Number')
    )
    group = models.ForeignKey(
        'SMSGroups',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('SMS Group')
    )


