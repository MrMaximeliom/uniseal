from rest_framework import serializers


class  CitySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  City
        model =  City
        fields = "__all__"

class  CountrySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Country
        model = Country
        fields = "__all__"

class  StateSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  State
        model = State
        fields = "__all__"

class  AreaSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  Area
        model = Area
        fields = "__all__"