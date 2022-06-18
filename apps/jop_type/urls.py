from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from Util.search_form_strings import DELETE_JOB_TYPES_TITLE, EDIT_JOB_TYPES_TITLE, ALL_JOB_TYPES_TITLE, \
    ADD_JOB_TYPES_TITLE
from apps.common_code.views import UpdateModelView, AddModelView, ModelDeleteView
from apps.jop_type.dashboard_views import JobTypeListView
from apps.jop_type.models import JopType

urlpatterns = [
    path('allJobTypes', staff_member_required(JobTypeListView.as_view(
        model=JopType,
        template_name="job_type/all_job_types.html",
        main_active_flag="job",
        active_flag="all_job_types",
        model_name="JobType",
        title=ALL_JOB_TYPES_TITLE,
    ), login_url="login"), name="jobTypesList"),
    path('addJobTypes', staff_member_required(AddModelView.as_view(
        model=JopType,
        fields=['name'],
        main_active_flag="job",
        active_flag="add_job_types",
        reference_field_name="name",
        template_name="job_type/add_job_types.html",
        title=ADD_JOB_TYPES_TITLE,
        success_url="jobTypesList"
    ), login_url="login"), name="addJobTypes"),
    path('editJobTypes', staff_member_required(JobTypeListView.as_view(
        model=JopType,
        template_name="job_type/edit_job_types.html",
        main_active_flag="job",
        active_flag="edit_job_types",
        model_name="JobType",
        title=EDIT_JOB_TYPES_TITLE
    ), login_url="login"), name="editJobTypes"),
    path('editJobType/<str:slug>/', staff_member_required(UpdateModelView.as_view(
        model=JopType,
        fields=['name'],
        main_active_flag="job",
        active_flag="edit_job_types",
        reference_field_name="name",
        template_name="job_type/edit_job_type.html",
        title=EDIT_JOB_TYPES_TITLE,
        success_url="jobTypesList"
    ), login_url="login"), name="editJobType"),
    path('deleteJobTypes', staff_member_required(JobTypeListView.as_view(
        model=JopType,
        template_name="job_type/delete_job_types.html",
        main_active_flag="job",
        active_flag="delete_job_types",
        model_name="JobType",
        title=DELETE_JOB_TYPES_TITLE
    ), login_url="login"), name="deleteJobTypes"),
    path('deleteJobType/<str:slug>/', staff_member_required(ModelDeleteView.as_view(
        model=JopType,
        main_active_flag="job",
        active_flag="delete_job_types",
        title=DELETE_JOB_TYPES_TITLE,
        success_url="jobTypesList"
    ), login_url="login"), name="deleteJobType"),
]