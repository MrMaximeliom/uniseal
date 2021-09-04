from django import forms
import datetime
from .models import Project,ProjectImages,ProjectVideos,Application
from django.utils.translation import gettext_lazy as _
from Util.utils import current_year


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]
# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         execution_date = forms.DateField(input_formats='YYYY-MM-DD',widget=forms.SelectDateWidget)
#         fields = ('name','title','category','beneficiary',
#                   'image','description','beneficiary_description','slug','execution_date')


class ProjectForm(forms.ModelForm):
    # name = forms.CharField(max_length=100,label=_('Project Name'),required=True)
    # title = forms.CharField(max_length=120,label=_('Project Title'),required=True)
    # category = forms.CharField(max_length=100,label=_('Project Category'),required=True)
    # beneficiary = forms.CharField(max_length=100,label=_('Project Beneficiary'),required=True)
    # image = forms.ImageField(required=True,label=_('Project Image'))
    # description = forms.CharField(widget=forms.Textarea,required=False,label=_('Project Description'))
    # beneficiary_description = forms.CharField(widget=forms.Textarea,required=False,label=_('Beneficiary Description'))
    # slug = forms.CharField(max_length=120,required=False,label=_('Project Slug'))
    # # execution_date = forms.DateField(input_formats='YYYY', widget=forms.SelectDateWidget,label=_('Project Execution Date'),required=True)
    # application = forms.ModelChoiceField(queryset=Application.objects.all())
    # execution_date = forms.DateField(input_formats='dd-mm-yyyy', widget=forms.SelectDateWidget,label=_('Project Execution Date'),required=True)
    # date = forms.CharField(max_length=100,required=False,label=_('Project Date'),attrs = {'placeholder': _('Select Project Date')})
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('slug',)
        widgets = {
            'date':forms.TextInput(attrs={'placeholder': _('Select Project Date')})
            }

class ProjectImagesForm(forms.ModelForm):
    from project.models import Project
    # project = forms.ChoiceField(required=False,
    #     choices=[(x.name) for x in Project.objects.all()]
    # )
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




















