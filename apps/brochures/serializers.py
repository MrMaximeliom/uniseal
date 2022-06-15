from rest_framework import serializers


class  BrochuresSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Brochures
        model =  Brochures
        fields = "__all__"