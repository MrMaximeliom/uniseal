from .models import Notifications
from django import forms


class NotificationsForm(forms.ModelForm):
    class Meta:
        model=Notifications
        fields='__all__'
        exclude = ('slug',)