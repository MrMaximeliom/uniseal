from rest_framework import viewsets
from uniseal.permissions import IsAdminOrReadOnly, IsAnonymousUser, \
    UnisealPermission, IsSystemBackEndUser

from django.utils.translation import gettext_lazy as _


# Create your views here.
class  BrochuresViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify brochures by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "title": "title",
        "attachment": "document_url_image",
    }
    Use PUT function by accessing this url:
    /brochures/<brochures's_id>
    Format of data will be as the previous data format for GET function

      """
    from brochures.serializers import BrochuresSerializer

    def get_view_name(self):
        return _("Create/Modify Selling Point Contact Info")

    from brochures.models import Brochures
    queryset = Brochures.objects.all()
    serializer_class = BrochuresSerializer
    permission_classes = [UnisealPermission]
