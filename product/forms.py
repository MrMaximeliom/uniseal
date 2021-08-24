from .models import Product,ProductImages
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('slug',)

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = '__all__'

