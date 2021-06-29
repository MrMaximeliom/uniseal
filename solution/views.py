from django.shortcuts import render
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from uniseal.permissions import IsAdminOrReadOnly, IsAnonymousUser, \
    UnisealPermission, IsSystemBackEndUser


# Create your views here.

class SolutionViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify solutions' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
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
     "id":solution_image_id,
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
     "id":solution_image_id,
     "video": "solution_video_url",
     "solution":solution_id,
     }
     Use other functions by accessing this url:
     solution/solutionVideos/<solutionVideos'_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Solution Videos")

    from .serializers import SolutionVideosSerializer
    serializer_class = SolutionVideosSerializer
    from .models import SolutionVideos
    permission_classes = [UnisealPermission]
    queryset = SolutionVideos.objects.all()
