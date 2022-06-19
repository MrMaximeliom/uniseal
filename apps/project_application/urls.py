from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView
from apps.project.models import Application
from apps.project_application.dashboard_views import ProjectApplicationListView

urlpatterns = [
  path('allApplications', staff_member_required(ProjectApplicationListView.as_view(
    model=Application,
    template_name="project_application/all_applications.html",
    main_active_flag="project_types",
    active_flag="all_applications",
    model_name="Application",
    title="All Project's Types"
  ), login_url="login"), name="allApplications"),
  path('addApplications', staff_member_required(AddModelView.as_view(
    model=Application,
    fields=['name', 'arabic_name'],
    main_active_flag="project_types",
    active_flag="add_applications",
    reference_field_name="name",
    template_name="project_application/add_applications.html",
    title="Add Project's Types",
    success_url="allApplications"
  ), login_url="login"), name="addApplications"),
  path('deleteApplications', staff_member_required(ProjectApplicationListView.as_view(
    model=Application,
    template_name="project_application/delete_projects.html",
    main_active_flag="project_types",
    active_flag="delete_applications",
    model_name="Application",
    title="Delete Projects' Types"
  ), login_url="login"), name="deleteApplications"),
  path('editApplications', staff_member_required(ProjectApplicationListView.as_view(
    model=Application,
    template_name="project_application/edit_applications.html",
    main_active_flag="project_types",
    active_flag="edit_applications",
    model_name="Application",
    title="Edit Projects' Types"
  ), login_url="login"), name="editApplications"),
  path('editApplication/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=Application,
        fields=['name', 'arabic_name'],
        main_active_flag="project_types",
        active_flag="edit_applications",
        reference_field_name="name",
        template_name="project_application/edit_application.html",
        title="Edit Projects' Types",
        success_url="allApplications"
    ), login_url="login"), name="editApplication"),
  path('deleteApplication/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
    model=Application,
    main_active_flag="project_types",
    active_flag="delete_applications",
    model_name='Application',
    title="Delete Projects' Types",
    success_url="allApplications"
  ), login_url="login"), name="deleteApplication"),
  ]