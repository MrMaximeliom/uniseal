from rest_framework import serializers

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



class SimilarProductSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import SimilarProduct
        model = SimilarProduct
        fields = "__all__"
