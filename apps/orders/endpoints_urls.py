from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets,permissions
from Util.permissions import UnisealPermission
from django_filters.rest_framework import DjangoFilterBackend



class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify orders' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "status": "order_status",
     }
     Use other functions by accessing this url:
     orders/<order's_id>
    """

    def get_view_name(self):
        return _("Create/Modify Orders' Data")

    from .serializers import OrderSerializer
    serializer_class = OrderSerializer
    from .models import Order
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status','user']


class CartViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify carts by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":10,
     "user": user_id,
     "product":product_id,
     "order":order_id,
     "quantity":quantity,
     }
     Use other functions by accessing this url:
     cart/cart's_id>
     Format of data will be as the previous data format for GET function
    """
    def get_view_name(self):
        return _("Create/Modify Carts")
    from .serializers import CartSerializer
    serializer_class = CartSerializer
    from .models import Cart
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cart.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product','order']

