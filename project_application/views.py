from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from Util.permissions import UnisealPermission
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Util.utils import  SearchMan,createExelFile,ReportMan,delete_temp_folder
from django.contrib.admin.views.decorators import staff_member_required

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
    queryset = Application.objects.all().order_by('id')
    serializer_class = ProjectApplicationSerializer
    permission_classes = [UnisealPermission]

from project.models import Application
applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
searchManObj = SearchMan("Application")
report_man = ReportMan()
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    project_list = []
    application_list = []
    headers_here = ["Project Type", "Number of Projects"]
    if headers is not None:
        print("in selected query headers are not none")
        headers_here = headers
        for header in headers_here:
            if header == "Project Type":
                for page in selected_pages:
                    for application in paginator_obj.page(page):
                        application_list.append(application.name)
            elif header == "Number of Projects":
                for page in selected_pages:
                    print("in for loop for supplier website")
                    for application in paginator_obj.page(page):
                        project_list.append(application.num_projects)
    else:
        print("in selected query headers are not none")
        for page in range(1, paginator_obj.num_pages+1):
            for application in paginator_obj.page(page):
                project_list.append(application.num_projects)
                application_list.append(application.name)
    return headers_here, application_list , project_list
def prepare_query(paginator_obj,headers=None):
    application_list = []
    project_list = []
    headers_here = ["Project Type","Number of Projects"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Project Type":
                for page in range(1, paginator_obj.num_pages+1):
                    for application in paginator_obj.page(page):
                        application_list.append(application.name)
            elif header == "Number of Projects":
                for page in range(1, paginator_obj.num_pages+1):

                    for application in paginator_obj.page(page):
                        project_list.append(application.num_projects)
    else:

        for page in range(1, paginator_obj.num_pages+1):
            for application in paginator_obj.page(page):
                application_list.append(application.name)
                project_list.append(application.num_projects)
    return headers_here, application_list, project_list
@staff_member_required(login_url='login')
def all_applications(request):
    from project.models import Application
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PROJECT_APPLICATION_NAME_SYNTAX_ERROR

    )
    all_applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
    paginator = Paginator(all_applications, 5)
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Application.objects.annotate(num_projects=Count('project')).filter(name=search_message).order_by('-num_projects')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Project Type')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter project type  first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
        searchManObj.setPaginator(all_applications)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_applications = Application.objects.annotate(num_projects=Count('project')).order_by('-num_projects')
        searchManObj.setPaginator(all_applications)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Project Type")
        headers.append("Number of Projects")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, application_list ,project_list = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(application_list) > 0:
                    constructor.update({"application": application_list})
                if len(project_list) > 0:
                    constructor.update({"num_projects": project_list})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Project_Types',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Project Type", "Number of Projects"]
                headers, application_list , project_list = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Project_Types',
                                                                                  headers, application=application_list,
                                                                                  num_projects=project_list
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = searchManObj.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers,  application_list , project_list = prepare_query(query,headers=headers)
                if len(application_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"application": application_list})
                if len(project_list) > 0:
                    print("project list is bigger than 0")
                    constructor.update({"num_projects": project_list})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Project_Types',
                                                                                  headers, **constructor)
                if status:

                   request.session['temp_dir'] = 'delete man!'
                   messages.success(request, f"Report Successfully Created ")
                   # return redirect('download_file',filepath=filepath,filename=filename)

                   return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, application_list,project_list = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Project_Types',
                                                                                  headers,application=application_list,
                                                                                  num_projects=project_list)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
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
                      'title': _('All Project Types'),
                      'all_applications': 'active',
                      'all_applications_data': application,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "application_error": PROJECT_APPLICATION_NAME_SYNTAX_ERROR,
                      }
                  }
                  )
@staff_member_required(login_url='login')
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
        'title': _('Add Project Types'),
        'add_applications': 'active',
        'form': form,
    }
    return render(request, 'project_application/add_applications.html', context)
@staff_member_required(login_url='login')
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
                      'title': _('Delete Project Types'),
                      'delete_applications': 'active',
                      'all_applications_data': applications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
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
                      'title': _('Edit Project Types'),
                      'edit_applications': 'active',
                      'all_applications_data': applications,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@staff_member_required(login_url='login')
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
        'title': _('Edit Project Types'),
        'edit_applications': 'active',
        'all_applications': all_applications,
        'form': application_form,
        'application': obj,
    }
    return render(request, 'project_application/edit_application.html', context)
@staff_member_required(login_url='login')
def confirm_delete(request,id):
    from project.models import Application
    obj = get_object_or_404(Application, id=id)
    try:
        obj.delete()
        messages.success(request, f"Application {obj.name} deleted successfully")
    except:
        messages.error(request, f"Application {obj.name} was not deleted , please try again!")


    return redirect('deleteApplications')