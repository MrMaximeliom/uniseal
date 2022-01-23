from rest_framework import serializers


class  ManageProductsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ManageProducts
        model =  ManageProducts
        fields = "__all__"

class  ManageProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ManageProjects
        model =  ManageProjects
        fields = "__all__"


class  ManageSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ManageSolution
        model =  ManageSolution
        fields = "__all__"

class  ManageSellingPointsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ManageSellingPoints
        model =  ManageSellingPoints
        fields = "__all__"

class  ManageBrochuresSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ManageBrochures
        model =  ManageBrochures
        fields = "__all__"