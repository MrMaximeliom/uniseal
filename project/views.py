from Util.permissions import UnisealPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render


class ProjectViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to add or modify projects' data
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":id,
     "name": "project_name",
     "title":"project_title",
     "category":"project_category",
     "beneficiary":"beneficiary_name",
     "image":"project_image_url",
     "description":"project_description",
     }
     Use other functions by accessing this url:
     project/createProject/<project's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Projects")

    from .serializers import ProjectSerializer
    serializer_class = ProjectSerializer
    from .models import Project
    permission_classes = [UnisealPermission]
    queryset = Project.objects.all()


class ProjectImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify projects' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":5,
     "image": "project_image_url",
     "project":project_id
     }
     Use other functions by accessing this url:
     project/projectImage/<project's_id>
     Format of data will be as the previous data format for GET function
     To Get All Project's Images use this url:
     project/projectImage/?project=<project's_id>
    """

    def get_view_name(self):
        return _("Create/Modify Project Images")

    from .serializers import ProjectImageSerializer
    serializer_class = ProjectImageSerializer
    from .models import ProjectImages
    permission_classes = [UnisealPermission]
    queryset = ProjectImages.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']


class ProjectVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify project' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id":7,
         "video": "project_video_url",
         "project":project_id
         }
         Use other functions by accessing this url:
         project/projectVideo/<projectVideo's_id>
         Format of data will be as the previous data format for GET function
         To Get All Project's Videos use this url:
         project/projectVideo/?project=<project's_id>

        """

    def get_view_name(self):
        return _("Create/Modify Projects Videos")

    from .serializers import ProjectVideoSerializer
    serializer_class = ProjectVideoSerializer
    from .models import ProjectVideos
    permission_classes = [UnisealPermission]
    queryset = ProjectVideos.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

class ProjectSolutionViewSet(viewsets.ModelViewSet):
    """API endpoint to add solutions to projects by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id": 9,
         "project":project_id,
         "solution":solution_id,
         }
         Use other functions by accessing this url:
         project/projectSolution/<projectSolution's_id>
         Format of data will be as the previous data format for GET function
         To Get All projects that have used the same solution use this url:
         project/projectSolution/?solution=<solution_id>
         To Get All solutions that have been used in the same project :
         project/projectSolution/?project=<project_id>
        """

    def get_view_name(self):
        return _("Add/Remove Projects Solutions")

    from .serializers import ProjectSolutionSerializer
    serializer_class = ProjectSolutionSerializer
    from .models import ProjectSolutions
    permission_classes = [UnisealPermission]
    queryset = ProjectSolutions.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project','solution']

#Views for dashboard

def all_projects(request):
    from project.models import Project
    all_projects = Project.objects.all()
    context = {
        'title': _('All Projects'),
        'all_projects': 'active',
        'all_projects_data': all_projects,
    }
    return render(request, 'project/all_projects.html', context)

def add_projects(request):
    from project.models import Project
    all_projects = Project.objects.all()
    context = {
        'title': _('Add Projects'),
        'add_projects': 'active',
        'all_projects': all_projects,
    }
    return render(request, 'project/add_projects.html', context)

def delete_projects(request):
    from project.models import Project
    all_projects = Project.objects.all()
    context = {
        'title': _('Delete Projects'),
        'delete_projects': 'active',
        'all_projects': all_projects,
    }
    return render(request, 'project/delete_projects.html', context)

def edit_projects(request):
    from project.models import Project
    all_projects = Project.objects.all()
    context = {
        'title': _('Edit Projects'),
        'edit_projects': 'active',
        'all_projects': all_projects,
    }
    return render(request, 'project/edit_projects.html', context)
