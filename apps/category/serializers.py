from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Category
        model = Category
        fields = "__all__"