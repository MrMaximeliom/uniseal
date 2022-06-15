from django.urls import path

from apps.company_info import views as company_views

urlpatterns = [
    path('companyDetails', company_views.company_details, name='CompanyDetails'),
    path('editCompanyDetails', company_views.edit_info, name='EditCompanyDetails'),
    path('addCompanyDetails', company_views.AddDetailsFormView.as_view(), name='AddCompanyDetails'),
    ]