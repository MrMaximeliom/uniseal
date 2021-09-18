from django import forms

from .models import ProductApplicationVideos


class ApplicationVideoForm(forms.ModelForm):
    class Meta:
        model = ProductApplicationVideos
        fields = '__all__'
        exclude = ('slug',)



