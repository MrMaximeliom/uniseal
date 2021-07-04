from Util.permissions import UnisealPermission
from rest_framework import viewsets

# Create your views here.
from django.utils.translation import gettext_lazy as _


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

    from .serializers import SellingPointSerializer
    serializer_class = SellingPointSerializer
    from .models import SellingPoint
    permission_classes = [UnisealPermission]
    queryset = SellingPoint.objects.all()



# class  SellingPointsContactInfoViewSet(viewsets.ModelViewSet):
#     """
#         API endpoint that allows to add selling points contact info
#         this endpoint allows  GET,POST,PUT,PATCH,DELETE function
#         permissions to this view is restricted as the following:
#         - only admin users can access this api
#          Data will be retrieved in the following format using GET function:
#        {
#         "id": 26,
#         "primary_phone": primary_phone,
#         "secondary_phone": secondary_phone,
#     }
#     Use PUT function by accessing this url:
#     /sellingPoint/contactInfo/<sellingPointContactInfo's_id>
#     Format of data will be as the previous data format for GET function
#
#       """
#     from .serializers import SellingPointsContactInfoSerializer
#
#     def get_view_name(self):
#         return _("Create/Modify Selling Point Contact Info")
#
#     from .models import SellingPointsContactInfo
#     queryset = SellingPointsContactInfo.objects.all()
#     serializer_class = SellingPointsContactInfoSerializer
#     permission_classes = [UnisealPermission]
#
