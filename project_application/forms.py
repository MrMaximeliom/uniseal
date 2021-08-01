from django import forms
class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        from project_application.models import Application
        model = Application
        fields = '__all__'




















