from rest_framework import serializers
# from apps.product.serializers import ProductSerializer



class ManageProductsSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=False, read_only=True)
    # product_id = serializers.IntegerField(write_only=True)
    class Meta:
        from .models import ManageProducts

        model = ManageProducts
        fields = "__all__"


class ManageProductsPageSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageProductsPage
        model = ManageProductsPage
        fields = "__all__"


class ManageProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageProjects
        model = ManageProjects
        fields = "__all__"


class ManageSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageSolution
        model = ManageSolution
        fields = "__all__"


class ManageSellingPointsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageSellingPoints
        model = ManageSellingPoints
        fields = "__all__"


class ManageBrochuresSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageBrochures
        model = ManageBrochures
        fields = "__all__"


class ManageOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ManageCarts
        model = ManageCarts
        fields = "__all__"
