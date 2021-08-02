from django import forms
from .models import WorkingField

class WorkingFieldForm(forms.ModelForm):
    class Meta:
        model = WorkingField
        fields = '__all__'
        exclude = ('slug',)