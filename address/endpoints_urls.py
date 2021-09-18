from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets

from Util.permissions import UnisealPermission


class CityViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify cities by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "city_name",
        "state": state_id,
       }
      Use PUT function by accessing this url:
      /address/modifyCity/<city's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CitySerializer

    def get_view_name(self):
        return _("Create/Modify Cities' Data")

    from address.models import City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [UnisealPermission]


class CountryViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify countries by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "country_name",

       }
      Use PUT function by accessing this url:
      /address/modifyCountry/<country's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CountrySerializer

    def get_view_name(self):
        return _("Create/Modify Countries' Data")

    from address.models import Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [UnisealPermission]


class StateViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify states by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "country_name",
        "country": country_id,

       }
      Use PUT function by accessing this url:
      /address/modifyState/<country's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import StateSerializer

    def get_view_name(self):
        return _("Create/Modify States' Data")

    from address.models import State
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [UnisealPermission]


class AreaViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify areas by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "area_name",
        "city": city_id,

       }
      Use PUT function by accessing this url:
      /address/modifyArea/<area's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import AreaSerializer

    def get_view_name(self):
        return _("Create/Modify Areas' Data")

    from address.models import Area
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [UnisealPermission]

