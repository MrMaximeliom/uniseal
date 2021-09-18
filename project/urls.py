from django.urls import path

from project import dashboard_views as project_views

urlpatterns = [
    path('allProjects', project_views.all_projects, name='allProjects'),
    path('addProjects', project_views.add_projects, name='addProjects'),
    path('deleteProjects', project_views.delete_projects, name='deleteProjects'),
    path('deleteProject/<int:id>', project_views.confirm_delete, name='deleteProject'),
    path('editProjects', project_views.edit_projects, name='editProjects'),
    path('editProject/<str:slug>', project_views.edit_project, name='editProject'),
    path('projectDetails/<str:slug>', project_views.project_details, name='projectDetails'),
    path('projectImages/<str:slug>', project_views.project_images, name='projectImages'),
    path('projectImages/', project_views.project_images, name='projectImages-dash'),

    ]