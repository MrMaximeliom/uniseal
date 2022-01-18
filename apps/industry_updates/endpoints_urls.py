from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets

from Util.permissions import UnisealPermission


class IndustryUpdateViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify industry updates' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id": 12,
     "headline":"headline content",
     "link":"url_link",
     }
     Use other functions by accessing this url:
     industryUpdates/<update's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Industry Updates")

    from .serializers import IndustryUpdatesSerializer
    serializer_class = IndustryUpdatesSerializer
    from .models import IndustryUpdates
    permission_classes = [UnisealPermission]
    queryset = IndustryUpdates.objects.all().order_by('-date')
#Views for dashboard
from .models import IndustryUpdates
updates = IndustryUpdates.objects.all().order_by('-id')
