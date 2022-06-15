from django import forms

from .models import Approval, ApprovalImage


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields ='__all__'
        exclude = ('slug',)



class ApprovalImagesForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    approval = forms.ModelMultipleChoiceField(
        queryset=Approval.objects.all()
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        pub = self.cleaned_data['approval']
        instance.approval = pub[0]
        instance.save(commit)
        return instance
    class Meta:
        model = ApprovalImage
        fields = ('image',)