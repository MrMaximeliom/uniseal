from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from Util.permissions import UnisealPermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

class SolutionViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify solutions' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":12,
     "title": "solution_title",
     "description":"solution_description",
     }
     Use other functions by accessing this url:
     solution/<solution's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Solution")

    from .serializers import SolutionSerializer
    serializer_class = SolutionSerializer
    from .models import Solution
    permission_classes = [UnisealPermission]
    queryset = Solution.objects.all()

class SolutionImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify solutions images' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "image": "solution_image_url",
     "solution":solution_id,
     }
     Use other functions by accessing this url:
     solution/solutionImages/<solutionImages'_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Solution Images")

    from .serializers import SolutionImagesSerializer
    serializer_class = SolutionImagesSerializer
    from .models import SolutionImages
    permission_classes = [UnisealPermission]
    queryset = SolutionImages.objects.all()

class SolutionVideosViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify solutions videos' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "video": "solution_video_url",
     "solution":solution_id,
     }
     Use other functions by accessing this url:
     solution/solutionVideos/<solutionVideos'_id>
     Format of data will be as the previous data format for GET function
     To Get All Solution's Videos for one solution use this url:
     solution/solutionVideos/?solution=<solution_id>
    """

    def get_view_name(self):
        return _("Create/Modify Solution Videos")

    from .serializers import SolutionVideosSerializer
    serializer_class = SolutionVideosSerializer
    from .models import SolutionVideos
    permission_classes = [UnisealPermission]
    queryset = SolutionVideos.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['solution']

#Views for dashboard
from solution.models import Solution
solutions = Solution.objects.all()
@login_required(login_url='login')
def all_solutions(request):
    # from solution.models import Solution
    # all_solutions = Solution.objects.all()
    context = {
        'title': _('All Solutions'),
        'all_solutions': 'active',
        'all_solutions_data': solutions,
    }
    return render(request, 'solution/all_solutions.html', context)
@login_required(login_url='login')
def add_solutions(request):

    context = {
        'title': _('Add Solutions'),
        'add_solutions': 'active',
        'all_solutions': solutions,
    }
    return render(request, 'solution/add_solutions.html', context)
@login_required(login_url='login')
def delete_solutions(request):

    context = {
        'title': _('Delete Solutions'),
        'delete_solutions': 'active',
        'all_solutions': solutions,
    }
    return render(request, 'solution/delete_solutions.html', context)
@login_required(login_url='login')
def edit_solutions(request):
    context = {
        'title': _('Edit Solutions'),
        'edit_solutions': 'active',
        'all_solutions': solutions,
    }
    return render(request, 'solution/edit_solutions.html', context)
