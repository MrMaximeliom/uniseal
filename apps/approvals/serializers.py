from rest_framework import serializers




class  ApprovalImagesSerializer(serializers.ModelSerializer):
    # approval = ApprovalSerializer(many=False, read_only=True)
    # approval_id = serializers.IntegerField(write_only=True)
    class Meta:
        from .models import  ApprovalImage
        model =  ApprovalImage
        fields = "__all__"
class  ApprovalSerializer(serializers.ModelSerializer):
    approval_images = ApprovalImagesSerializer(many=True, read_only=True)
    class Meta:
        from .models import  Approval
        model =  Approval
        fields = "__all__"