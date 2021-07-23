from .models import Product,ProductImages,ProductVideos
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductVideosForm(forms.ModelForm):
    class Meta:
        model = ProductVideos
        fields = '__all__'