from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from Util.permissions import UnisealPermission,IsConsultantUser
from django_filters.rest_framework import DjangoFilterBackend


class  RequestAccessViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to accept or revoke
         request access permissions by the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "status": "access_status",
        "user":2,
        }
    Use PUT function by accessing this url:
    /requestAccess/<request's_id>
    Format of data will be as the previous data format for GET function
    """
    from .serializers import RequestAccessSerializer

    def get_view_name(self):
        return _("Create/Update Request Access Data")

    from .models import RequestAccess
    queryset = RequestAccess.objects.all()
    serializer_class = RequestAccessSerializer
    permission_classes = [IsConsultantUser,UnisealPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

