from django.urls import path

from apps.jop_type import dashboard_views as jop_type_views

urlpatterns = [
    path('allJobTypes', jop_type_views.JopTypeListView.as_view(), name='jobTypesList'),
    path('addJobTypes', jop_type_views.JopTypeFormView.as_view(), name='addJobTypes'),
    path('editJobTypes', jop_type_views.JopTypeListView.as_view(), name='editJobTypes'),
]