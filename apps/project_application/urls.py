from django.urls import path

from apps.project_application import dashboard_views as application_views

urlpatterns = [
  path('allApplications', application_views.all_applications, name='allApplications'),
  path('addApplications', application_views.add_applications, name='addApplications'),
  path('deleteApplications', application_views.delete_applications, name='deleteApplications'),
  path('editApplications', application_views.edit_applications, name='editApplications'),
  path('editApplication/<str:slug>',application_views.edit_application, name='editApplication'),
  path('deleteApplication/<int:id>', application_views.confirm_delete, name='deleteApplication'),
  ]