from django.shortcuts import render
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from Util.permissions import UnisealPermission

# Create your views here.
class  CompanyInfoViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify company info by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "phone_number": 923432134,
          "email": "company@ema.com",
          "company_name":"company_name",
          "main_address":"Al-Khartoum,Jabrah,Sudan",
          "country":1,
          "state":1,
          "city":1.
          "website":"www.company.com",
          "facebook":"www.facebook/company",
          "twitter":"www.twitter/company",
          "linkedin":"www.linkedin/company",
          "instagram":"www.instagram/company",

         }
        Use PUT function by accessing this url:
        /companyInfo/<company'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import CompanyInfoSerializer

    def get_view_name(self):
        return _("Create/Modify Company's Data")

    from .models import CompanyInfo
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [UnisealPermission]