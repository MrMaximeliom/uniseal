from rest_framework import serializers

# Create your models here.
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Offer
        model = Offer
        fields = "__all__"

