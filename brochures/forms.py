from django import forms
from .models import Brochures

class BrochuresForm(forms.ModelForm):
    class Meta:
        model = Brochures
        fields = '__all__'