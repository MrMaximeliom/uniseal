from django import forms
from .models import ManageCarts, ManageSolution, ManageProducts, ManageProjects, \
    ManageProductsPage, ManageBrochures, ManageSellingPoints


class ManageProductsForm(forms.ModelForm):
    class Meta:
        model = ManageProducts
        fields = '__all__'


class ManageProductsPageForm(forms.ModelForm):
    class Meta:
        model = ManageProductsPage
        fields = '__all__'


class ManageSolutionForm(forms.ModelForm):
    class Meta:
        model = ManageSolution
        fields = '__all__'


class ManageProjectsForm(forms.ModelForm):
    class Meta:
        model = ManageProjects
        fields = '__all__'


class ManageCartsForm(forms.ModelForm):
    class Meta:
        model = ManageCarts
        fields = '__all__'


class ManageBrochuresForm(forms.ModelForm):
    class Meta:
        model = ManageBrochures
        fields = '__all__'


class ManageSellingPointsForm(forms.ModelForm):
    class Meta:
        model = ManageSellingPoints
        fields = '__all__'
