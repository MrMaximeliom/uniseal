from rest_framework import serializers


class  ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Approval
        model =  Approval
        fields = "__all__"

class  ApprovalImagesSerializer(serializers.ModelSerializer):
    approval = ApprovalSerializer(many=False, read_only=True)
    approval_id = serializers.IntegerField(write_only=True)
    class Meta:
        from .models import  ApprovalImage
        model =  ApprovalImage
        fields = "__all__"