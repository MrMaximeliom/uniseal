from rest_framework import viewsets
from rest_framework.views import APIView

from .permissions import IsAdminOrReadOnly, IsAnonymousUser, \
    UnisealPermission, IsSystemBackEndUser

from django.utils.translation import gettext_lazy as _


# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify suppliers' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Other users can only use GET function on this endpoint
    Data will be retrieved in the following format for GET function:
    {
     "name": "supplier_name",
     "image": "supplier_image_url",
     }
     Use other functions by accessing this url:
     supplier/<supplier's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Suppliers' Data")

    from .serializers import SupplierSerializer
    serializer_class = SupplierSerializer
    from .models import Supplier
    permission_classes = [IsAdminOrReadOnly]
    queryset = Supplier.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
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

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer
    from .models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all()


class ProductImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "image": "product_image_url",
     "product":product_id
     }
     Use other functions by accessing this url:
     productImage/<productImage's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Products Images")

    from .serializers import ProductImageSerializer
    serializer_class = ProductImageSerializer
    from .models import ProductImages
    permission_classes = [UnisealPermission]
    queryset = ProductImages.objects.all()


class ProductVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "video": "product_video_url",
         "product":product_id
         }
         Use other functions by accessing this url:
         productVideo/<productVideo's_id>
         Format of data will be as the previous data format for GET function
        """

    def get_view_name(self):
        return _("Create/Modify Products Videos")

    from .serializers import ProductVideoSerializer
    serializer_class = ProductVideoSerializer
    from .models import ProductVideos
    permission_classes = [UnisealPermission]
    queryset = ProductVideos.objects.all()


class SimilarProductViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Link/Unlink Similar Products")

    from .serializers import SimilarProductSerializer
    serializer_class = SimilarProductSerializer
    from .models import SimilarProduct
    permission_classes = [UnisealPermission]
    queryset = SimilarProduct.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to add or modify projects' data
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "name": "project_name",
     "category":"project_category",
     "image":"project_image_url",
     "description":"project_description",
     }
     Use other functions by accessing this url:
     project/<project's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Projects")

    from .serializers import ProjectSerializer
    serializer_class = ProjectSerializer
    from .models import Project
    permission_classes = [UnisealPermission]
    queryset = Project.objects.all()


class ProjectImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify projects' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "image": "project_image_url",
     "project":project_id
     }
     Use other functions by accessing this url:
     projectImage/<project's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Project Images")

    from .serializers import ProjectImageSerializer
    serializer_class = ProjectImageSerializer
    from .models import ProjectImages
    permission_classes = [UnisealPermission]
    queryset = ProjectImages.objects.all()


class ProjectVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify project' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "video": "project_video_url",
         "product":project_id
         }
         Use other functions by accessing this url:
         projectVideo/<projectVideo's_id>
         Format of data will be as the previous data format for GET function
        """

    def get_view_name(self):
        return _("Create/Modify Projects Videos")

    from .serializers import ProjectVideoSerializer
    serializer_class = ProjectVideoSerializer
    from .models import ProjectVideos
    permission_classes = [UnisealPermission]
    queryset = ProjectVideos.objects.all()


class SellingPointViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify selling points' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "name": "selling_point_name",
     "image":"selling_point_image_url",
     "location":"selling_point_location",
     "address":"selling_point_address",
     }
     Use other functions by accessing this url:
     sellingPoint/<sellingPoint's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Selling Points")

    from .serializers import SellingPointSerializer
    serializer_class = SellingPointSerializer
    from .models import SellingPoint
    permission_classes = [UnisealPermission]
    queryset = SellingPoint.objects.all()


class Logout(APIView):
    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework.response import Response
        from rest_framework import status
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class  SellingPointsContactInfoViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add selling points contact info
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "primary_phone": primary_phone,
        "secondary_phone": secondary_phone,
    }
    Use PUT function by accessing this url:
    /sellingPoint/contactInfo/<sellingPointContactInfo's_id>
    Format of data will be as the previous data format for GET function

      """
    from uniseal.serializers import SellingPointsContactInfoSerializer

    def get_view_name(self):
        return _("Create/Modify Selling Point Contact Info")

    from uniseal.models import SellingPointsContactInfo
    queryset = SellingPointsContactInfo.objects.all()
    serializer_class = SellingPointsContactInfoSerializer
    permission_classes = [UnisealPermission]


class  BrochuresViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify brochures by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "title": "title",
        "attachment": "document_url_image",
    }
    Use PUT function by accessing this url:
    /brochures/<brochures's_id>
    Format of data will be as the previous data format for GET function

      """
    from uniseal.serializers import SellingPointsContactInfoSerializer

    def get_view_name(self):
        return _("Create/Modify Selling Point Contact Info")

    from uniseal.models import SellingPointsContactInfo
    queryset = SellingPointsContactInfo.objects.all()
    serializer_class = SellingPointsContactInfoSerializer
    permission_classes = [UnisealPermission]


class  ContactUsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify messages by
        registered users
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions  this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "phone_number": phone_number,
        "email": "email",
        "name": "name",
        "address": "address",
        "message": "message",
        "website": "website_url",
        "facebook": "facebook_url",
        "twitter": "twitter_url",
        "linkedin": "linkedin_url",
        "instagram": "instagram_url",
    }
    Use PUT function by accessing this url:
    /contactUs/<contactUsMessages's_id>
    Format of data will be as the previous data format for GET function

      """
    from uniseal.serializers import SellingPointsContactInfoSerializer

    def get_view_name(self):
        return _("Create/Modify Selling Point Contact Info")

    from uniseal.models import SellingPointsContactInfo
    queryset = SellingPointsContactInfo.objects.all()
    serializer_class = SellingPointsContactInfoSerializer
    permission_classes = [UnisealPermission]