from .models import Notifications
from django import forms


class NotificationsForm(forms.ModelForm):
    from .models import TokenIDs
    # token_id = forms.ModelMultipleChoiceField(
    #     queryset=TokenIDs.objects.all(),
    #
    # )
    #
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     pub = self.cleaned_data['token_id']
    #     instance.token_id = pub[0]
    #     instance.save(commit)
    #     return instance
    class Meta:
        model=Notifications
        fields='__all__'
        exclude = ('slug',)