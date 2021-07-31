from django.urls import path
from sms_notifications import views as sms_notifications_views
urlpatterns = [
    path('allSMS', sms_notifications_views.all_sms, name='allSMS'),
    path('sendSMS', sms_notifications_views.send_sms, name='sendSMS'),
    path('addSMSGroup', sms_notifications_views.add_sms_group, name='addSMSGroup'),
    path('addSMSContact', sms_notifications_views.add_sms_contact, name='addSMSContact'),
    path('deleteSMS', sms_notifications_views.delete_sms, name='deleteSMS'),
    ]