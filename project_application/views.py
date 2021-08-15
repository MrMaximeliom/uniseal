from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from Util.permissions import UnisealPermission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
class  ProjectApplicationViewSet(viewsets.ModelViewSet):
    """
          API endpoint that allows to add or modify project application info by
          the admin
          this endpoint allows  GET,POST,PUT,PATCH,DELETE function
          permissions to this view is restricted as the following:
          - only admin users can access this api
           Data will be retrieved in the following format using GET function:
         {
          "id": 1,
          "name": "application_name",

         }
        Use PUT function by accessing this url:
        /projectApplication/<application's_id>
        Format of data will be as the previous data format for GET function
        """
    from .serializers import ProjectApplicationSerializer

    def get_view_name(self):
        return _("Create/Modify Project Application Data")

    from project.models import Application
    queryset = Application.objects.all()
    serializer_class = ProjectApplicationSerializer
    permission_classes = [UnisealPermission]

from project.models import Application
applications = Application.objects.all()
@login_required(login_url='login')
def all_applications(request):
    from project.models import Application
    all_applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
    paginator = Paginator(all_applications, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        application = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        application = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        application = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'project_application/all_applications.html',
                  {
                      'title': _('All Project Applications'),
                      'all_applications': 'active',
                      'all_applications_data': application,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def add_applications(request):
    from .forms import ProjectApplicationForm
    if request.method == 'POST':
        form = ProjectApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Project Application Added: {name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = ProjectApplicationForm()

    context = {
        'title': _('Add Project Applications'),
        'add_applications': 'active',
        'form': form,
    }
    return render(request, 'project_application/add_applications.html', context)
@login_required(login_url='login')
def delete_applications(request):
    from project.models import Application
    all_application = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
    paginator = Paginator(all_application, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        applications = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        applications = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        applications = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'project_application/delete_applications.html',
                  {
                      'title': _('Delete Project Applications'),
                      'delete_applications': 'active',
                      'all_applications_data': applications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_applications(request):
    from project.models import Application
    all_applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
    paginator = Paginator(all_applications, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        applications = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        applications = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        applications = paginator.page(paginator.num_pages)
        page = paginator.num_pages



    return render(request, 'project_application/edit_applications.html',
                  {
                      'title': _('Edit Project Applications'),
                      'edit_applications': 'active',
                      'all_applications_data': applications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_application(request,slug):
    from project.models import Application
    from .forms import ProjectApplicationForm
    all_applications = Application.objects.all()
    # fetch the object related to passed id
    obj = get_object_or_404(Application, slug=slug)

    # pass the object as instance in form
    application_form = ProjectApplicationForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if application_form.is_valid():
        application_form.save()
        application_name = application_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {application_name} Data")
        application_form.save()
    else:
        for field, items in application_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Project Applications'),
        'edit_applications': 'active',
        'all_applications': all_applications,
        'form': application_form,
        'application': obj,
    }
    return render(request, 'project_application/edit_application.html', context)
def confirm_delete(request,id):
    from project.models import Application
    obj = get_object_or_404(Application, id=id)
    try:
        obj.delete()
        messages.success(request, f"Application {obj.name} deleted successfully")
    except:
        messages.error(request, f"Application {obj.name} was not deleted , please try again!")


    return redirect('deleteApplications')