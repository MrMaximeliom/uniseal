from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


# Create your views here.

class registerTokenIds(viewsets.ModelViewSet):
    """
          API endpoint that allows to register token ids data by the application automatically
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
          Data will be retrieved in the following format using GET function:
        {
        "id": 26,
        "token_id": "long_token",
        "os_type": "os_type",

    }
    Use PUT function by accessing this url:
    /notifications/registerTokenId/<token's_id>
    Format of data will be as the previous data format for GET function

    """
    from .serializers import TokensSerializer
    from .models import TokenIDs
    queryset = TokenIDs.objects.all()
    serializer_class = TokensSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reg_id']


    def get_view_name(self):
        return _("Register/Modify Token Ids")

class handleNotifications(viewsets.ModelViewSet):
    """
          API endpoint that allows to handle notifications by admin
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
          Data will be retrieved in the following format using GET function:
        {
        "id": 26,
        "token_id": "long_token",
        "title": "notification_title",
        "body":"notification_body",
        "notification_sending_date":"notification_sending_date",


    }
    Use PUT function by accessing this url:
    /notifications/handleNotifications/<notification's_id>
    Format of data will be as the previous data format for GET function

    """
    from .serializers import NotificationsSerializer
    from .models import Notifications
    queryset = Notifications.objects.all().order_by('-notification_date')
    serializer_class = NotificationsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['token_id',]


    def get_view_name(self):
        return _("Handle Notifications")
