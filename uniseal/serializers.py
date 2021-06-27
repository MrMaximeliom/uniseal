from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Supplier
        model = Supplier
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Product
        model = Product
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProductImages
        model = ProductImages
        fields = "__all__"


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProductVideos
        model = ProductVideos
        fields = "__all__"


class SimilarProductSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SimilarProduct
        model = SimilarProduct
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Project
        model = Project
        fields = "__all__"


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProjectImages
        model = ProjectImages
        fields = "__all__"


class ProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ProjectVideos
        model = ProjectVideos
        fields = "__all__"


class SellingPointSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SellingPoint
        model = SellingPoint
        fields = "__all__"