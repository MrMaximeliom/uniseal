from accounts.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields='__all__'

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email' , 'password']