from rest_framework import serializers

# Create your models here.
class RequestAccessSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import RequestAccess
        model = RequestAccess
        fields = "__all__"

