from django.urls import path
from sms_notifications import views as sms_notifications_views
urlpatterns = [
    path('allSMS', sms_notifications_views.all_sms, name='allSMS'),
    path('sendSMS', sms_notifications_views.send_sms, name='sendSMS'),
    path('sendSMSToSMSGroup', sms_notifications_views.send_sms_to_group, name='sendSMSToSMSGroup'),
    path('addSMSGroup', sms_notifications_views.add_sms_group, name='addSMSGroup'),
    path('addSMSContact', sms_notifications_views.add_sms_contact, name='addSMSContact'),
    path('editSMSNotifications', sms_notifications_views.edit_SMSs, name='editSMSs'),
    path('editSMSNotification/<str:slug>', sms_notifications_views.edit_sms, name='editSMS'),
    path('allSMSGroups', sms_notifications_views.all_sms_groups, name='allSMSGroups'),
    path('editSMSGroups', sms_notifications_views.edit_groups, name='editSMSGroups'),
    path('editSMSGroup/<str:slug>', sms_notifications_views.edit_group, name='editSMSGroup'),
    path('allSMSContacts', sms_notifications_views.all_sms_contacts, name='allSMSContacts'),
    path('editSMSContacts', sms_notifications_views.edit_contacts, name='editSMSContacts'),
    path('editSMSContact/<str:slug>', sms_notifications_views.edit_contact, name='editSMSContact'),
    path('deleteSMS', sms_notifications_views.delete_sms, name='deleteSMS'),
    path('deleteSMSNotification/<int:id>', sms_notifications_views.confirm_delete_sms_notification, name='deleteSMSNotification'),
    path('deleteSMSGroups', sms_notifications_views.delete_sms_group, name='deleteSMSGroups'),
    path('deleteSMSGroup/<int:id>', sms_notifications_views.confirm_delete_sms_group,name='deleteSMSGroup'),
    path('deleteSMSContacts', sms_notifications_views.delete_sms_contact, name='deleteSMSContacts'),
    path('deleteSMSContact/<int:id>', sms_notifications_views.confirm_delete_sms_group, name='deleteSMSContact'),
]
