from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from Util.permissions import UnisealPermission


class  JobTypeViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add jop types by the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "consultant",
        }
    Use PUT function by accessing this url:
    /jopType/<jopType's_id>
    Format of data will be as the previous data format for GET function
    """
    from .serializers import JopTypeSerializer

    def get_view_name(self):
        return _("Create/Update JobTypes' Data")

    from .models import JopType
    queryset = JopType.objects.all()
    serializer_class = JopTypeSerializer
    permission_classes = [UnisealPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

