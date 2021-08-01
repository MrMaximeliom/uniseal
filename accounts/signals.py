from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from .models import User
from django.dispatch import receiver
from sms_notifications.models import SMSContacts
# from django.contrib.auth import user_logged_in, user_logged_out
# from django.dispatch.dispatcher import receiver as receiver_second
# from django.contrib.sessions.models import Session


# عند تسجيل مستخدم جديد يتم إنشاء ملف شخصي خاص به تلقائيا
@receiver(post_save, sender=User)
def create_sms_contact(sender, instance, created, **kwargs):
    from sms_notifications.models import SMSGroups
    admin_sms_group = get_object_or_404(SMSGroups, id=1)
    users_sms_group = get_object_or_404(SMSGroups, id=2)
    if created:
        if instance.admin:
            new_contact = SMSContacts.objects.create(
                contact_number=instance.phone_number,
                group = admin_sms_group

            )
            new_contact.save()
        else:
            new_contact = SMSContacts.objects.create(
                contact_number=instance.phone_number,
                group = users_sms_group

            )
            new_contact.save()


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     # if instance.gender == 'Male':
#     #     instance.profile.image = "/profile_pics/default_male.jpg"
#     # else:
#     #     instance.profile.image = "/profile_pics/default_female.jpg"
#
#     instance.profile.save()

