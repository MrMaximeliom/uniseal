from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets

from Util.permissions import UnisealPermission


class ApprovalViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify approvals by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "approval_name",
        "image": "approval_image_path",
        "file": "approval_file_path",
       }
      Use PUT function by accessing this url:
      /approvals/<approval's_id>
      Format of data will be as the previous data format for GET function

      """
    from apps.approvals.serializers import ApprovalSerializer

    def get_view_name(self):
        return _("Create/Modify Approvals' Data")

    from apps.approvals.models import Approval
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [UnisealPermission]

class ApprovalImagesViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify approvals' images by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "image": "approval_image_path",
        "approval": 23,
       }
      Use PUT function by accessing this url:
      /approvals/approvalsImages/<approval's_id>
      Format of data will be as the previous data format for GET function

      """
    from apps.approvals.serializers import ApprovalImagesSerializer

    def get_view_name(self):
        return _("Create/Modify Approvals' Images Data")

    from apps.approvals.models import ApprovalImage
    queryset = ApprovalImage.objects.all()
    serializer_class = ApprovalImagesSerializer
    permission_classes = [UnisealPermission]