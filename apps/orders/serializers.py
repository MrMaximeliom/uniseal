from django import forms
from rest_framework import serializers

from apps.accounts.serializers import UserOrderSerializer
from apps.product.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    # user = UserSerializer(many=False, read_only=False)
    product_id = serializers.IntegerField(write_only=True)
    # user_id = serializers.IntegerField(write_only=True)
    class Meta:
        from .models import Cart
        model = Cart
        fields = "__all__"
        widgets = {
            'quantity': forms.TextInput(attrs={'min': '1'})
        }

class OrderSerializer(serializers.ModelSerializer):
    order_details = CartSerializer(many=True, read_only=True)
    user = UserOrderSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        from .models import Order
        model = Order
        fields = "__all__"