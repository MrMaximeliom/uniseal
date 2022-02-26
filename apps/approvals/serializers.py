from rest_framework import serializers


class  ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Approval
        model =  Approval
        fields = "__all__"