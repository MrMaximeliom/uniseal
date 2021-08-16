from rest_framework import serializers

class IndustryUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import IndustryUpdates
        model = IndustryUpdates
        fields = "__all__"