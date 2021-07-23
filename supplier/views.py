from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from Util.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify suppliers' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Other users can only use GET function on this endpoint
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "supplier_name",
     "image": "supplier_image_url",
     }
     Use other functions by accessing this url:
     supplier/<supplier's_id>
     Format of data will be as the previous data format for GET function
     To Search for particular supplier by its name use this url:
     supplier/?name=<supplier_name>
    """

    def get_view_name(self):
        return _("Create/Modify Suppliers' Data")


    from .serializers import SupplierSerializer
    serializer_class = SupplierSerializer

    def get_queryset(self):
        from .models import Supplier
        queryset = Supplier.objects.all().order_by("id")
        return queryset
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
