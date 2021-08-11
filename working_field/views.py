from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from rest_framework.permissions import IsAdminUser
# Create your views here.
class  WorkinFieldViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify working fields info by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "field_name": "working_field_name",

         }
        Use PUT function by accessing this url:
        /workingField/<field's_id>
        Format of data will be as the previous data format for GET function
        """
    from .serializers import WorkingFieldSerializer

    def get_view_name(self):
        return _("Create/Modify Working Field Data")

    from .models import WorkingField
    queryset = WorkingField.objects.all()
    serializer_class = WorkingFieldSerializer
    permission_classes = [IsAdminUser]

# Dashboard Views
from .models import WorkingField
from django.contrib.auth.decorators import login_required
fields = WorkingField.objects.all()
# fields = WorkingField.objects.annotate(num_users=Count('user')).order_by('-num_users')
@login_required(login_url='login')
def all_fields(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(fields, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        fields_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        fields_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        fields_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'working_field/all_fields.html',
                  {
                      'title': _('All Working Fields'),
                      'all_fields': 'active',
                      'all_fields_data': fields_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@login_required(login_url='login')
def add_fields(request):
    from .forms import WorkingFieldForm
    if request.method == 'POST':
        form = WorkingFieldForm(request.POST)
        if form.is_valid():
            form.save()
            field_name = form.cleaned_data.get('field_name')
            messages.success(request, f"New Working Field Added: {field_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = WorkingFieldForm()


    context = {
        'title': _('Add Working Fields'),
        'add_fields': 'active',
        'form': form,
    }
    return render(request, 'working_field/add_field.html', context)

@login_required(login_url='login')
def delete_fields(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(fields, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        fields_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        fields_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        fields_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'working_field/delete_fields.html',
                  {
                      'title': _('Delete Working Fields'),
                      'delete_fields': 'active',
                      'all_fields_data': fields_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@login_required(login_url='login')
def edit_fields(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(fields, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        fields_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        fields_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        fields_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'working_field/edit_fields.html',
                  {
                      'title': _('Edit Working Fields'),
                      'edit_fields': 'active',
                      'all_fields_data': fields_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_field(request,slug):
    from .models import WorkingField
    from .forms import WorkingFieldForm

    obj = get_object_or_404(WorkingField, slug=slug)

    # pass the object as instance in form
    working_form = WorkingFieldForm(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if working_form.is_valid():
        working_form.save()
        field_name = working_form.cleaned_data.get('field_name')
        messages.success(request, f"Successfully Updated : {field_name} Data")
    else:
        for field, items in working_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Working Fields'),
        'edit_fields': 'active',
        'form': working_form,
        'field': obj,

    }
    return render(request, 'working_field/edit_field.html', context)


def confirm_delete(request,id):
    from .models import WorkingField
    obj = get_object_or_404(WorkingField, id=id)
    try:
        obj.delete()
        messages.success(request, f"Working Field: {obj.field_name} deleted successfully")
    except:
        messages.error(request, f"Working Field: {obj.field_name} was not deleted , please try again!")


    return redirect('deleteFields')
