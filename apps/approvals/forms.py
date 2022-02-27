from django import forms

from .models import Approval,ApprovalImage


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields ='__all__'
        exclude = ('slug',)

class ApprovalImagesForm(forms.ModelForm):
    class Meta:
        model = ApprovalImage
        fields ='__all__'
        exclude = ('slug',)