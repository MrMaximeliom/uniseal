from django import forms
from .models import JopType


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JopType
        fields = '__all__'
        exclude = ('slug',)