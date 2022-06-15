from django.urls import path

from apps.request_permissions import dashboard_views as request_views

urlpatterns = [
    path('allRequests', request_views.RequestAccessListView.as_view(), name='requestAccessList'),
    path('updateRequest/<int:pk>', request_views.GiveOrDenyAccess, name='updateRequest'),
  ]