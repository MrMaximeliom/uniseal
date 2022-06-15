from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView, ModelListView
from apps.sms_notifications import dashboard_views as sms_notifications_views
from apps.sms_notifications.dashboard_views import SMSListView, SMSGroupsListView
from apps.sms_notifications.models import SMSNotification, SMSGroups, SMSContacts

urlpatterns = [
    path('allSMS', staff_member_required(SMSListView.as_view(
        model=SMSNotification,
        template_name="sms_notifications/sms/all_sms.html",
        main_active_flag="sms_notifications",
        active_flag="all_sms_notifications",
        model_name="SMSNotification",
        title="All SMS Notifications"
    ), login_url="login"), name="allSMS"),
    path('sendSMS', sms_notifications_views.send_sms, name='sendSMS'),
    path('sendSMSToSMSGroup', sms_notifications_views.send_sms_to_group, name='sendSMSToSMSGroup'),
    path('addSMSGroup', staff_member_required(AddModelView.as_view(
        model=SMSGroups,
        fields=['name', 'arabic_name'],
        main_active_flag="sms_notifications",
        active_flag="add_sms_group",
        reference_field_name="name",
        template_name="sms_notifications/groups/add_group.html",
        title="Add SMS Groups",
        success_url="allSMSGroups"
    ), login_url="login"), name="addSMSGroup"),
    path('addSMSContact', staff_member_required(AddModelView.as_view(
        model=SMSContacts,
        fields=['contact_number', 'group'],
        main_active_flag="sms_notifications",
        active_flag="add_sms_contact",
        reference_field_name="contact_number",
        template_name="sms_notifications/contacts/add_contact.html",
        title="Add SMS Contacts",
        success_url="allSMSContacts"
    ), login_url="login"), name="addSMSContact"),
    path('editSMSNotifications', staff_member_required(SMSListView.as_view(
        model=SMSNotification,
        template_name="sms_notifications/edit_SMSs.html",
        main_active_flag="sms_notifications",
        active_flag="edit_sms",
        model_name="SMSNotification",
        title="Edit SMS Notifications"
    ), login_url="login"), name="editSMSs"),
    path('editSMSNotification/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=SMSNotification,
        fields=['status', 'message',
                'single_mobile_number'],
        main_active_flag="sms_notifications",
        active_flag="edit_sms",
        reference_field_name="message",
        template_name="sms_notifications/sms/edit_sms.html",
        title="Edit SMS Notifications",
        success_url="allSMSNotifications"
    ), login_url="login"), name="editSMS"),
    path('allSMSGroups', staff_member_required(SMSListView.as_view(
        model=SMSNotification,
        template_name="sms_notifications/groups/all_groups.html",
        main_active_flag="sms_notifications",
        active_flag="all_groups",
        model_name="SMSGroups",
        title="All SMS Groups"
    ), login_url="login"), name="allSMSGroups"),
    path('editSMSGroups', staff_member_required(SMSGroupsListView.as_view(
        model=SMSGroups,
        template_name="sms_notifications/groups/edit_groups.html",
        main_active_flag="sms_notifications",
        active_flag="edit_groups",
        model_name="SMSGroups",
        title="Edit SMS Groups"
    ), login_url="login"), name="editSMSGroups"),
    path('editSMSGroup/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=SMSGroups,
        fields=['name', 'arabic_name'],
        main_active_flag="sms_notifications",
        active_flag="edit_groups",
        reference_field_name="name",
        template_name="sms_notification/groups/edit_group.html",
        title="Edit SMS Notifications",
        success_url="allSMSGroupNotification"
    ), login_url="login"), name="editSMSGroup"),
    path('allSMSContacts', staff_member_required(ModelListView.as_view(
        model=SMSContacts,
        template_name="sms_notifications/contacts/all_contacts.html",
        main_active_flag="sms_notifications",
        active_flag="all_contacts",
        model_name="SMSContacts",
        title="All SMS Contacts"
    ), login_url="login"), name="allSMSContacts"),
    path('editSMSContacts', staff_member_required(ModelListView.as_view(
        model=SMSContacts,
        template_name="sms_notifications/contacts/edit_contacts.html",
        main_active_flag="sms_notifications",
        active_flag="edit_contacts",
        model_name="SMSContacts",
        title="Edit SMS Contacts"
    ), login_url="login"), name="editSMSContacts"),
    path('editSMSContact/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=SMSContacts,
        fields=['contact_number', 'group'],
        main_active_flag="sms_notifications",
        active_flag="edit_sms_contact",
        reference_field_name="contact_number",
        template_name="sms_notifications/contacts/edit_contact.html",
        title="Edit SMS Contacts",
        success_url="allSMSContacts"
    ), login_url="login"), name="editSMSContact"),
    path('deleteSMS', staff_member_required(ModelListView.as_view(
        model=SMSNotification,
        template_name="sms_notifications/sms/delete_sms.html",
        main_active_flag="sms_notifications",
        active_flag="delete_sms",
        model_name="SMSNotification",
        title="Delete SMS Notifications"
    ), login_url="login"), name="deleteSMS"),
    path('deleteSMSNotification/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=SMSNotification,
        main_active_flag="sms_notifications",
        active_flag="delete_sms",
        model_name='SMSNotification',
        title="Delete SMS Notifications",
        success_url="deleteSMS"
    ), login_url="login"), name="deleteSMSNotification"),
    path('deleteSMSGroups', staff_member_required(ModelListView.as_view(
        model=SMSGroups,
        template_name="sms_notifications/groups/delete_groups.html",
        main_active_flag="sms_notifications",
        active_flag="delete_groups",
        model_name="SMSGroups",
        title="Delete SMS Groups"
    ), login_url="login"), name="deleteSMSGroups"),
    path('deleteSMSGroup/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=SMSGroups,
        main_active_flag="sms_notifications",
        active_flag="delete_groups",
        model_name='SMSGroups',
        title="Delete SMS Groups",
        success_url="allSMSGroups"
    ), login_url="login"), name="deleteSMSGroup"),
    path('deleteSMSContacts', staff_member_required(ModelListView.as_view(
        model=SMSContacts,
        template_name="sms_notifications/contacts/delete_contacts.html",
        main_active_flag="sms_notifications",
        active_flag="delete_contacts",
        model_name="SMSContacts",
        title="Delete SMS Contacts"
    ), login_url="login"), name="deleteSMSContacts"),
    path('deleteSMSContact/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=SMSContacts,
        main_active_flag="sms_notifications",
        active_flag="delete_contacts",
        model_name='SMSContacts',
        title="Delete SMS Contacts",
        success_url="deleteSMSContacts"
    ), login_url="login"), name="deleteSMSContact"),
]
