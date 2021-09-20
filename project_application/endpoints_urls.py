from rest_framework import viewsets

from Util.permissions import UnisealPermission

from django.utils.translation import gettext_lazy as _

# Create your views here.
class  ProjectApplicationViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify project application info by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "name": "application_name",

         }
        Use PUT function by accessing this url:
        /projectApplication/<application's_id>
        Format of data will be as the previous data format for GET function
        """
    from .serializers import ProjectApplicationSerializer

    def get_view_name(self):
        return _("Create/Modify Project Application Data")

    from project.models import Application
    queryset = Application.objects.all().order_by('id')
    serializer_class = ProjectApplicationSerializer
    permission_classes = [UnisealPermission]
