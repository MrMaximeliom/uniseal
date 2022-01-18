from rest_framework import serializers
class SellingPointSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SellingPoint
        model = SellingPoint
        fields = "__all__"

