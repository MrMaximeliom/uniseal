from rest_framework import serializers

# Create your models here.
class ProductApplicationVideoSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProductApplicationVideos
        model = ProductApplicationVideos
        fields = "__all__"

