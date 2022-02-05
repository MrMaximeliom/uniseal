# from django.db.models.signals import post_save
# from apps.accounts.models import User
# from django.dispatch import receiver
#
# #عند تسجيل مستخدم جديد يتم إنشاء ملف شخصي خاص به تلقائيا
# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,**kwargs):
#     if created:
#          new_profile = Profile.objects.create(user=instance)
#          # new_profile.image = "/profile_pics/default_male.jpg"
#          # تكون الصورة الشخصية مطابقة لجنس المستخدم الجديد
#
#          if instance.gender == 'Male':
#              if instance.is_teacher == 1:
#                  new_profile.image = "/profile_pics/teacher_male.jpg"
#              else:
#                  new_profile.image = "/profile_pics/boy_student.jpg"
#          else:
#              if instance.is_teacher == 1:
#                  new_profile.image = "/profile_pics/female_teacher.jpg"
#              else:
#                  new_profile.image = "/profile_pics/girl_student.jpg"
#
#
#
# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#     # if instance.gender == 'Male':
#     #     instance.profile.image = "/profile_pics/default_male.jpg"
#     # else:
#     #     instance.profile.image = "/profile_pics/default_female.jpg"
#
#     instance.profile.save()
#
# # Test to link session to user
# # @receiver_second(user_logged_in)
# # def remove_other_sessions(sender, user, request, **kwargs):
# #     # remove other sessions
# #     Session.objects.filter(usersession__user=user).delete()
# #
# #     # save current session
# #     request.session.save()
# #
# #     # create a link from the user to the current session (for later removal)
# #     UserSession.objects.get_or_create(
# #         user=user,
# #         session=Session.objects.get(pk=request.session.session_key)
# #     )
# # @receiver(user_logged_in)
# # def on_user_logged_in(sender, request, **kwargs):
# #     LoggedInUser.objects.get_or_create(user=kwargs.get('user'))
# #
# #
# # @receiver(user_logged_out)
# # def on_user_logged_out(sender, **kwargs):
# #     LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
