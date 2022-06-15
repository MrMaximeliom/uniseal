from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.common_code.views import ModelDeleteView, AddModelView, UpdateModelView
from apps.project import dashboard_views as project_views
from apps.project.dashboard_views import ProjectListView
from apps.project.models import Project

urlpatterns = [
    path('allProjects', staff_member_required(ProjectListView.as_view(
        model=Project,
        template_name="project/all_projects.html",
        main_active_flag="projects",
        active_flag="all_projects",
        model_name="Project",
        title="All Projects"
    ), login_url="login"), name="allProjects"),
    path('topProjects', project_views.top_projects, name='topProjects'),
    path('addProjects', staff_member_required(AddModelView.as_view(
        model=Project,
        fields=['name', 'arabic_name',
                'beneficiary', 'main_material', 'project_type',
                'description', 'arabic_description',
                'date', 'rank', 'is_top', 'image'],
        main_active_flag="projects",
        active_flag="add_projects",
        reference_field_name="name",
        template_name="project/add_projects.html",
        title="Add Projects",
        success_url="allProjects"
    ), login_url="login"), name="addProjects"),
    path('deleteProjects', staff_member_required(ProjectListView.as_view(
        model=Project,
        template_name="project/delete_projects.html",
        main_active_flag="projects",
        active_flag="delete_projects",
        model_name="Project",
        title="Delete Projects"
    ), login_url="login"), name="deleteProjects"),
    path('deleteProject/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Project,
        main_active_flag="projects",
        active_flag="delete_projects",
        model_name='Project',
        title="Delete Projects",
        success_url="deleteProjects"
    ), login_url="login"), name="deleteProject"),
    path('editProjects', staff_member_required(ProjectListView.as_view(
        model=Project,
        template_name="project/edit_projects.html",
        main_active_flag="projects",
        active_flag="edit_projects",
        model_name="Project",
        title="Edit Projects"
    ), login_url="login"), name="editProjects"),
    path('editProject/<str:slug>', staff_member_required(UpdateModelView.as_view(
        model=Project,
        fields=['name', 'arabic_name',
                'beneficiary', 'main_material', 'project_type',
                'description', 'arabic_description',
                'date', 'rank', 'is_top', 'image'],
        main_active_flag="projects",
        active_flag="edit_projects",
        reference_field_name="name",
        template_name="project/edit_project.html",
        title="Edit Projects",
        success_url="allProjects"
    ), login_url="login"), name="editProject"),
    path('projectDetails/<str:slug>', project_views.project_details, name='projectDetails'),
    path('projectImages/<str:slug>', project_views.project_images, name='projectImages'),
    path('projectImages/', project_views.project_images, name='projectImages-dash'),

    ]