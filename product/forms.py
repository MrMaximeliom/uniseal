from django import forms

from .models import Product, ProductImages


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('slug',)

class ProductImagesForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    product = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all()
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        pub = self.cleaned_data['product']
        instance.product = pub[0]
        instance.save(commit)
        return instance
    class Meta:
        model = ProductImages
        fields = ('image',)

