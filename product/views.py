from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets , mixins
from django_filters.rest_framework import DjangoFilterBackend
from Util.permissions import UnisealPermission
from django.shortcuts import render


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

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer
    from .models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category','supplier']


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


class ProductVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id":id,
         "video": "product_video_url",
         "product":product_id
         }
         Use other functions by accessing this url:
         product/productVideo/<productVideo's_id>
         Format of data will be as the previous data format for GET function
         To Get All Product's Videos for one product use this url:
         product/productVideo/?product=<product_id>
        """

    def get_view_name(self):
        return _("Create/Modify Products Videos")

    from .serializers import ProductVideoSerializer
    serializer_class = ProductVideoSerializer
    from .models import ProductVideos
    permission_classes = [UnisealPermission]
    queryset = ProductVideos.objects.all()
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


class FetchProductsByCategoryViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
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

    # from .models import Product
    # queryset = Product.objects.all()

    def get_queryset(self):
        from .models import Product
        # returning default result if anything goes wrong
        queryset = Product.objects.all()
        # category = self.request.query_params.get('category_id')
        category = self.kwargs['category_id']
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


#Views for product

def all_products(request):
    from product.models import Product
    all_products = Product.objects.all()
    context = {
        'title': _('All Products'),
        'all_products': 'active',
        'all_products_data': all_products,
    }
    if request.method == "GET":
        print("hi")
        params = request.GET
        param_list = list(params.items())
        print(param_list)
        for value in request.GET.items():
            print(value)
        # print(request.GET['a'])
    return render(request, 'product/all_products.html', context)
def add_products(request):
    from product.models import Product
    from category.models import Category
    from supplier.models import Supplier
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    all_suppliers =Supplier.objects.all()
    context = {
        'title': _('Add Products'),
        'add_products': 'active',
        'all_products': all_products,
        'all_categories':all_categories,
        'all_suppliers':all_suppliers,
    }
    return render(request, 'product/add_products.html', context)
def delete_products(request):
    from product.models import Product
    all_products = Product.objects.all()
    context = {
        'title': _('Delete Products'),
        'delete_products': 'active',
        'all_products': all_products,
    }
    return render(request, 'product/delete_products.html', context)
def edit_products(request):
    from product.models import Product
    all_products = Product.objects.all()
    context = {
        'title': _('Edit Products'),
        'edit_products': 'active',
        'all_products': all_products,
    }
    return render(request, 'product/edit_products.html', context)