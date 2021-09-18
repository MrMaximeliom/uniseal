# from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from Util.permissions import UnisealPermission


# Create your views here.
class  ProductApplicationVideosViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add product application videos
        by the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "application_video": "application_video_url",
        "product": product_id,
    }
    Use PUT function by accessing this url:
    /applicationVideos/productAppVideo/<video's_id>
    Format of data will be as the previous data format for GET function

      """
    from .serializers import ProductApplicationVideoSerializer

    def get_view_name(self):
        return _("Create/Update Product Application Videos' Data")

    from .models import ProductApplicationVideos
    queryset = ProductApplicationVideos.objects.all()
    serializer_class = ProductApplicationVideoSerializer
    permission_classes = [UnisealPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
