from .models import ProductApplicationVideos
from django import forms

class ApplicationVideoForm(forms.ModelForm):
    class Meta:
        model = ProductApplicationVideos
        fields = '__all__'
        exclude = ('slug',)



