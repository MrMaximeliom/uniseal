from django.urls import path
from notifications import views as notifications_views
urlpatterns = [
    path('allNotifications', notifications_views.all_notifications, name='allNotifications'),
    # path('addUsers', accounts_views.add_users, name='addUsers'),
    # path('deleteUsers', accounts_views.delete_users, name='deleteUsers'),
    # path('deleteUser/<int:id>/<str:url>', accounts_views.confirm_delete, name='deleteUser'),
    # path('editUser/<str:slug>', accounts_views.edit_user, name='editUser'),
    # path('editUsers', accounts_views.edit_users, name='editUsers'),
    # path('changePassword', accounts_views.change_password, name='changePassword'),
    # path('downloadReport/<path:file_path>/<str:file_name>', download_file,name='downloadReport'),
]