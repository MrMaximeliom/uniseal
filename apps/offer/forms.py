from django import forms

from .models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'
        exclude = ('slug',)