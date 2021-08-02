from rest_framework import serializers

class WorkingFieldSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import WorkingField
        model = WorkingField
        fields = "__all__"
