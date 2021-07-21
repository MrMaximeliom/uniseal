from django import forms
from .models import SMSNotification
from .models import SMSGroups
from .models import SMSContacts

class SMSNotificationForm(forms.ModelForm):
    class Meta:
        model = SMSNotification
        fields = '__all__'

class SMSGroupsForm(forms.ModelForm):
    class Meta:
        model = SMSGroups
        fields = '__all__'

class SMSContactsForm(forms.ModelForm):
    class Meta:
        model = SMSContacts
        fields = '__all__'