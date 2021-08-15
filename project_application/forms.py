from django import forms
class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        from project.models import Application
        model = Application
        fields = '__all__'
        exclude = ('slug',)




















