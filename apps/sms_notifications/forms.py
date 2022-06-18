from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import SMSNotification, SMSGroups, SMSContacts, SMSGroupMessages


class SMSNotificationForm(forms.ModelForm):
    class Meta:
        phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
                                     message=_("Phone number must start with 9 or 1 and includes 9 numbers."))
        single_mobile_number = forms.CharField(
            label=_('Single Mobile Numbser'),
            max_length=20,
            required=False,
            validators=[phone_regex],

        )
        model = SMSNotification
        widgets = {
            'single_mobile_number': forms.TextInput(attrs={'placeholder': '9xxxxxxxx'}),
        }
        fields = '__all__'
        exclude = ('slug',)

class SMSGroupsForm(forms.ModelForm):
    class Meta:
        model = SMSGroups
        fields = '__all__'
        exclude = ('slug',)

class SMSContactsForm(forms.ModelForm):
    class Meta:
        model = SMSContacts
        fields = '__all__'
        exclude = ('slug',)

class  SMSGroupMessagesForm(forms.ModelForm):
    class Meta:
        model = SMSGroupMessages
        fields = '__all__'
        exclude = ('slug',)