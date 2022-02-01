from rest_framework import serializers

# Create your models here.
class JopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import JopType
        model = JopType
        fields = "__all__"

