from rest_framework import serializers

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Supplier
        model = Supplier
        fields = "__all__"
