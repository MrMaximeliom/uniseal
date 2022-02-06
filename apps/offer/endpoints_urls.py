from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from Util.permissions import UnisealPermission


class  OfferViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add offers by the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "image": "offer_image_path",
        "offer_created_date":22-10-2022,
        "offer_start_date":22-10-2022,
        "offer_end_date":24-10-2022,
        }
    Use PUT function by accessing this url:
    /offers/<offer's_id>
    Format of data will be as the previous data format for GET function
    """
    from .serializers import OfferSerializer

    def get_view_name(self):
        return _("Create/Update Offers' Data")

    from .models import Offer
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [UnisealPermission]

