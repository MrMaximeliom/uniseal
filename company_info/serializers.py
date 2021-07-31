from rest_framework import serializers


class  CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  CompanyInfo
        model =  CompanyInfo
        fields = "__all__"