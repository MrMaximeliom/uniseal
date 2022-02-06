from django.urls import path

from apps.jop_type import dashboard_views as jop_type_views
from Util.search_form_strings import DELETE_JOB_TYPES_TITLE,EDIT_JOB_TYPES_TITLE

urlpatterns = [
    path('allJobTypes', jop_type_views.JopTypesListView.as_view(), name='jobTypesList'),
    path('addJobTypes', jop_type_views.JopTypeFormView.as_view(), name='addJobTypes'),
    path('editJobTypes', jop_type_views.JopTypesListView.as_view(template_name ="job_type/edit_job_types.html", active_flag="edit_job_types",title=EDIT_JOB_TYPES_TITLE), name='editJobTypes'),
    path('editJobType/<str:slug>/', jop_type_views.JopTypeUpdateView.as_view(), name='editJobType'),
    path('deleteJobTypes', jop_type_views.JopTypesListView.as_view(template_name ="job_type/delete_job_types.html", active_flag="delete_job_types",title=DELETE_JOB_TYPES_TITLE), name='deleteJobTypes'),
    path('deleteJobType/<str:slug>/', jop_type_views.confirm_delete, name='deleteJobType'),
]