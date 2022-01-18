from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets

from Util.permissions import UnisealPermission


class SellingPointViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify selling points' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":12,
     "name": "selling_point_name",
     "image":"selling_point_image_url",
     "location":"selling_point_location",
     "address":"selling_point_address",
     "city":"city_id",
     "area":"area_id",
     "phone_number":"phone_number",
     "secondary_phone":"secondary_phone_number",
     "email":"email",
     }
     Use other functions by accessing this url:
     sellingPoint/createSellingPoint/<sellingPoint's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Selling Points")
    def get_queryset(self):
        from .models import SellingPoint
        queryset = SellingPoint.objects.all().order_by('id')
        return queryset


    from .serializers import SellingPointSerializer
    serializer_class = SellingPointSerializer

    permission_classes = [UnisealPermission]




