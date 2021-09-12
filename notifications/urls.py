from django.urls import path, include
from notifications import views as notifications_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'notifications/registerTokenId', notifications_views.registerTokenIds, basename='RegisterNotifications')
router.register(r'notifications/handleNotifications', notifications_views.handleNotifications, basename='HandleNotifications')

urlpatterns = [
    path('allNotifications', notifications_views.all_notifications, name='allNotifications'),
    path('sendNotifications', notifications_views.send_notifications, name='sendNotifications'),
    path('deleteNotifications', notifications_views.delete_notifications, name='deleteNotifications'),
    path('deleteNotifications/<int:id>', notifications_views.confirm_delete, name='deleteNotification'),
    # path('editUser/<str:slug>', accounts_views.edit_user, name='editUser'),
    path('resendNotifications', notifications_views.edit_notifications, name='resendNotifications'),
    # path('changePassword', accounts_views.change_password, name='changePassword'),
    # path('downloadReport/<path:file_path>/<str:file_name>', download_file,name='downloadReport'),


]
