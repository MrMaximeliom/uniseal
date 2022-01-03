from rest_framework import serializers
from django import forms


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Cart
        model = Cart
        fields = "__all__"
        widgets = {
            'quantity': forms.TextInput(attrs={'min': '1'})
        }

class OrderSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True, read_only=True)
    class Meta:
        from .models import Order
        model = Order
        fields = [
            'id', 'status', 'carts','created_at','modified_at'
        ]

