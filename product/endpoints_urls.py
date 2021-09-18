from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from Util.permissions import UnisealPermission


# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "product_name",
     "image": "product_image_url",
     "product_file":"product_file_url",
     "description":"Product_description",
     "added_date":"added_date"
     "category":category_id,
     "supplier":"supplier_id",
     }
     Use other functions by accessing this url:
     product/modifyProduct/<product's_id>
     Format of data will be as the previous data format for GET function
     To Get Products By Category use this url:
     product/modifyProduct/?category=<category_id>
     To Get Products By Supplier use this url:
     product/modifyProduct/?supplier=<supplier_id>
     To Get Products By Both Category and Supplier use this url:
     product/modifyProduct/?category=<category_id>&supplier=<supplier_id>

    """

    def get_view_name(self):
        return _("Create/Modify Products' Data")

    # def get_queryset(self):
    #     from .models import Product
    #     # returning default result if anything goes wrong
    #     queryset = Product.objects.all().order_by("id")
    #     return queryset

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer
    from .models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all().order_by('is_top').order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'supplier','is_top']


class ProductImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":10,
     "image": "product_image_url",
     "product":product_id
     }
     Use other functions by accessing this url:
     product/productImage/<productImage's_id>
     Format of data will be as the previous data format for GET function
     To Get All Product's Images for one product use this url:
     product/productImage/?product=<product_id>
    """

    def get_view_name(self):
        return _("Create/Modify Products Images")

    from .serializers import ProductImageSerializer
    serializer_class = ProductImageSerializer
    from .models import ProductImages
    permission_classes = [UnisealPermission]
    queryset = ProductImages.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class SimilarProductViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Link/Unlink Similar Products")

    from .serializers import SimilarProductSerializer
    serializer_class = SimilarProductSerializer
    from .models import SimilarProduct
    permission_classes = [UnisealPermission]
    queryset = SimilarProduct.objects.all()


class FetchProductsByCategoryViewSet(generics.ListAPIView):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Fetch Products By Category")

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer

    permission_classes = [UnisealPermission]

    from .models import Product
    queryset = Product.objects.all()

    # original get_queryset
    def get_queryset(self):
        from .models import Product
        # returning default result if anything goes wrong
        queryset = Product.objects.all()
        # category = self.request.query_params.get('category_id')
        category = self.kwargs['category_id']
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

