from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from Util.permissions import UnisealPermission


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
