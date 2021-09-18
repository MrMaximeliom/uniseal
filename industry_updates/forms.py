from django import forms

from .models import IndustryUpdates


class IndustryUpdatesForm(forms.ModelForm):
    class Meta:
        model = IndustryUpdates
        fields = '__all__'
        exclude = ('slug',)