from django import forms

from .models import RequestAccess


class RequestAccessForm(forms.ModelForm):
    class Meta:
        model = RequestAccess
        fields = '__all__'
        exclude = ('slug',)