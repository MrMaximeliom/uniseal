
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from Util.permissions import UnisealPermission


# Create your views here.
class  ManageProductsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the products by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "product": product_id,
        "user": user_id,
        "product_views": product_views_count,
        "product_sheet_downloads": product_sheet_downloads_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageProducts/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageProductsSerializer

    def get_view_name(self):
        return _("Manage Products' data")

    from apps.admin_panel.models import ManageProducts
    queryset = ManageProducts.objects.all()
    serializer_class = ManageProductsSerializer
    permission_classes = [IsAuthenticated]

class  ManageProductsPageViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the products page by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "user": user_id,
        "product_page_views": product_page_views_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageProductsPage/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageProductsPageSerializer

    def get_view_name(self):
        return _("Manage Products Page's data")

    from apps.admin_panel.models import ManageProductsPage
    queryset = ManageProductsPage.objects.all()
    serializer_class = ManageProductsPageSerializer
    permission_classes = [IsAuthenticated]

class  ManageProjectsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the projects by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "project": project_id,
        "user": user_id,
        "project_views": project_views_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageProjects/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageProjectsSerializer

    def get_view_name(self):
        return _("Manage Projects' data")

    from apps.admin_panel.models import ManageProjects
    queryset = ManageProjects.objects.all()
    serializer_class = ManageProjectsSerializer
    permission_classes = [IsAuthenticated]

class  ManageSolutionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the solutions by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "solution": solution_id,
        "user": user_id,
        "solution_views": solution_views_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageSolution/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageSolutionSerializer

    def get_view_name(self):
        return _("Manage Solutions' data")

    from apps.admin_panel.models import ManageSolution
    queryset = ManageSolution.objects.all()
    serializer_class = ManageSolutionSerializer
    permission_classes = [IsAuthenticated]

class  ManageSellingPointsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the selling points by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "selling_point": selling_point_id,
        "user": user_id,
        "phone_number_clicks": phone_number_clicks_count,
        "secondary_phone_number": secondary_phone_number_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageSellingPoints/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageSellingPointsSerializer

    def get_view_name(self):
        return _("Manage Selling Points' data")

    from apps.admin_panel.models import ManageSellingPoints
    queryset = ManageSellingPoints.objects.all()
    serializer_class = ManageSellingPointsSerializer
    permission_classes = [IsAuthenticated]


class  ManageBrochuresViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the brochures by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "brochures": brochures_id,
        "user": user_id,
        "brochures_views": brochures_views_count,
        "brochures_sheet_downloads": brochures_sheet_downloads_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageBrochures/<record's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.admin_panel.serializers import ManageBrochuresSerializer

    def get_view_name(self):
        return _("Manage Brochures' data")

    from apps.admin_panel.models import ManageBrochures
    queryset = ManageBrochures.objects.all()
    serializer_class = ManageBrochuresSerializer
    permission_classes = [IsAuthenticated]

class  ManageCartsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to get reports about the carts by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "cart": cart_id,
        "user": user_id,
        "add_to_cart_views": cart_views_count,
    }
    Use PUT function by accessing this url:
    api/admin_panel/manageCarts/<record's_id>
    Format of data will be as the previous data format for GET function
      """
    from apps.admin_panel.serializers import ManageCartsSerializer

    def get_view_name(self):
        return _("Manage Carts' data")

    from apps.admin_panel.models import ManageCarts
    queryset = ManageCarts.objects.all()
    serializer_class = ManageCartsSerializer
    permission_classes = [IsAuthenticated]
