from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from rest_framework import viewsets, mixins

from Util.permissions import UnisealPermission
from Util.utils import EnablePartialUpdateMixin
from .forms import CompanyInfoForm


# Create your views here.
class  CompanyInfoViewSet(EnablePartialUpdateMixin, viewsets.GenericViewSet,
                          mixins.UpdateModelMixin,mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    """
          API endpoint that allows to add or modify company info by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "phone_number": 923432134,
          "email": "company@ema.com",
          "company_name":"company_name",
          "main_address":"Al-Khartoum,Jabrah,Sudan",
          "country":1,
          "state":1,
          "city":1.
          "website":"www.company.com",
          "facebook":"www.facebook/company",
          "twitter":"www.twitter/company",
          "linkedin":"www.linkedin/company",
          "instagram":"www.instagram/company",

         }
        Use PUT function by accessing this url:
        /companyInfo/<company'_id>
        Format of data will be as the previous data format for GET function

        """
    from .serializers import CompanyInfoSerializer

    def get_view_name(self):
        return _("Create/Modify Company's Data")

    from .models import CompanyInfo
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [UnisealPermission]
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required(login_url='login')
def edit_info(request):
    from .models import CompanyInfo
    from .forms import CompanyInfoForm
    # fetch the object related to passed id
    # obj = get_object_or_404(CompanyInfo, id=1)
    obj = CompanyInfo.objects.first()
    # pass the object as instance in form
    company_form = CompanyInfoForm(request.POST or None, instance=obj)
    if company_form.is_valid():
        company_form.save()
        messages.success(request, "The Company Info Has Been Updated Successfully!")
    else:
        for field, items in company_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))
    context = {
        'title': _('Edit Company Info'),
        'company_info': 'active',
        'form': company_form,
        'company': obj,
    }
    return render(request, 'company_info/edit_info.html', context)

class AddDetailsFormView(FormView):
    template_name = 'company_info/add_company_details.html'
    form_class = CompanyInfoForm
    success_url = 'CompanyDetails'
    def get(self, request, *args, **kwargs):
        from apps.company_info.models import CompanyInfo
        info = CompanyInfo.objects.count()
        if info == 0:
            self.extra_context = {
                 'company_info': 'active',
                 'title':"Add Company Info",
                 'is_initial_setup':True
            }
        else:
            self.extra_context = {
                'company_info': 'active',
                'title': "Add Company Info",
                'is_initial_setup': False
            }
        return super(AddDetailsFormView, self).get(self)

    def form_invalid(self, form):
        for field, items in form.errors.items():
            for item in items:
                print('{}: {}'.format(field, item))
        messages.error(self.request, "Company Details  did not added , please try again!")
        return super(AddDetailsFormView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, f"Company Details Added Successfully")
        return redirect(self.success_url)
    extra_context = {
        'company_info': 'active',
        'title':"Add Company Info"
    }
@staff_member_required(login_url='login')
def company_details(request):
    from apps.company_info.models import CompanyInfo
    company = CompanyInfo.objects.first()
    return render(request, 'company_info/info_detail.html',
                  {
                      'title': _('Company Details'),
                      'company_info': 'active',
                      'company_data': company,})