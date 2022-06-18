from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from apps.notifications.dashboard_views import NotificationListView,send_notifications
from apps.common_code.views import ModelDeleteView
from apps.notifications.models import Notifications
urlpatterns = [
    path('allNotifications', staff_member_required(NotificationListView.as_view(
        model=Notifications,
        template_name="notifications/all_notifications.html",
        main_active_flag="notifications",
        active_flag="all_notifications",
        model_name="Notifications",
        title="All Notifications"
    ), login_url="login"), name="allNotifications"),
    path('sendNotifications', send_notifications, name='sendNotifications'),
    path('deleteNotifications', staff_member_required(NotificationListView.as_view(
        model=Notifications,
        template_name="notifications/delete_notifications.html",
        main_active_flag="notifications",
        active_flag="delete_notifications",
        model_name="Notifications",
        title="All Notifications"
    ), login_url="login"), name="deleteNotifications"),
    path('deleteNotifications/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Notifications,
        main_active_flag="notifications",
        active_flag="delete_notifications",
        model_name='Notifications',
        title="Delete Notifications",
        success_url="deleteNotifications"
    ), login_url="login"), name="deleteNotifications"),


]
