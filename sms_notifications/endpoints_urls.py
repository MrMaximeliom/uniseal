from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser


# Create your views here.

class  SMSGroupsViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms groups data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "name":"group_name",
          "group_created_datetime": "auto_generated_datetime",

         }
        Use PUT function by accessing this url:
        /sms/<smsGroups'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSGroupsSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Groups data")

    from .models import SMSGroups
    queryset = SMSGroups.objects.all()
    serializer_class = SMSGroupsSerializer
    permission_classes = [IsAdminUser]

class  SMSNotificationViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms notifications data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "sender":"sender_name",
          "message":"message",
          "group": 1,
          "single_mobile_number": "249999627379",
          "is_multiple":false,
         }
        Use PUT function by accessing this url:
        /sms/<smsNotifications'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSNotificationSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Notifications data")

    from .models import SMSNotification
    queryset = SMSNotification.objects.all()
    serializer_class = SMSNotificationSerializer
    permission_classes = [IsAdminUser]

class  SMSContactsViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify sms contacts data by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "contact_number":"249999627379",
          "group": 1,
         }
        Use PUT function by accessing this url:
        /sms/<smsContacts'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import SMSContactsSerializer

    def get_view_name(self):
        return _("Create/Modify SMS Contacts data")

    from .models import SMSContacts
    queryset = SMSContacts.objects.all()
    serializer_class = SMSContactsSerializer
    permission_classes = [IsAdminUser]

