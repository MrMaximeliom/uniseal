import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, ProjectImages, ProjectVideos


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]
# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         execution_date = forms.DateField(input_formats='YYYY-MM-DD',widget=forms.SelectDateWidget)
#         fields = ('name','title','category','beneficiary',
#                   'image','description','beneficiary_description','slug','execution_date')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('slug',)
        widgets = {
            'date':forms.TextInput(attrs={'placeholder': _('Select Project Date')})
            }

class ProjectImagesForm(forms.ModelForm):
    from project.models import Project
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    project = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all()
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        pub = self.cleaned_data['project']
        instance.project = pub[0]
        instance.save(commit)
        return instance
    class Meta:
        model = ProjectImages
        fields = ('image',)

class ProjectVideosForm(forms.ModelForm):
    class Meta:
        model = ProjectVideos
        fields = '__all__'




















