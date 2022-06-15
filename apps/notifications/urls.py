from django.urls import path

from apps.notifications import dashboard_views as notifications_views

urlpatterns = [
    path('allNotifications', notifications_views.all_notifications, name='allNotifications'),
    path('sendNotifications', notifications_views.send_notifications, name='sendNotifications'),
    path('deleteNotifications', notifications_views.delete_notifications, name='deleteNotifications'),
    path('deleteNotifications/<int:id>', notifications_views.confirm_delete, name='deleteNotification'),
    path('resendNotifications', notifications_views.edit_notifications, name='resendNotifications'),


]
