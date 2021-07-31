from django import forms
from .models import Slider


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        exclude = ('slug',)