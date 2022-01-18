from rest_framework import serializers


class  SliderSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Slider
        model =  Slider
        fields = "__all__"