from rest_framework import generics

from .permissions import IsAdminOrReadOnly, IsAnonymousUser, \
    UnisealPermission, IsSystemBackEndUser

from django.utils.translation import gettext_lazy as _


class ProductViewSet(generics.ListAPIView,generics.CreateAPIView):
    """API endpoint to add or modify products' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "name": "product_name",
     "image": "product_image_url",
     "category":"product_category",
     "product_file":"product_file_url",
     "description":"Product_description",
     "supplier_name":"supplier_name",
     "added_name":"added_dated"
     }
     Use other functions by accessing this url:
     product/<product's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Products' Data")

    from product.serializers import ProductSerializer
    serializer_class = ProductSerializer
    from product.models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all()







