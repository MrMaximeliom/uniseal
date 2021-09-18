from django import forms

from .models import SellingPoint


class SellingPointForm(forms.ModelForm):
    class Meta:
        model = SellingPoint
        fields = '__all__'
        exclude = ('slug',)