from django import forms
from .models import Country,State,City,Area

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields ='__all__'
        exclude = ('slug',)

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields ='__all__'
        exclude = ('slug',)

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields ='__all__'
        exclude = ('slug',)

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields ='__all__'
        exclude = ('slug',)