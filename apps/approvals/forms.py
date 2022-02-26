from django import forms

from .models import Approval


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields ='__all__'
        exclude = ('slug',)