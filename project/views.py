from django.template.defaultfilters import slugify
from Util.permissions import UnisealPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from  django.contrib import messages
from django.contrib.auth.decorators import login_required
from Util.utils import  SearchMan,createExelFile,ReportMan,delete_temp_folder
from Util.utils import rand_slug
from django.db.models import Count

class ProjectViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to add or modify projects' data
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":id,
     "name": "project_name",
     "beneficiary":"beneficiary_name",
     "description":"project_description",
     "beneficiary_description":"project_beneficiary_description",
     "main_material":"project_main_material_used",
     "project_type":project_type_id,
     "execution_date":"project_execution_date",
     "date":"project_date",
     }
     Use other functions by accessing this url:
     project/createProject/<project's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Projects")

    from .serializers import ProjectSerializer
    serializer_class = ProjectSerializer
    from .models import Project
    permission_classes = [UnisealPermission]
    queryset = Project.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project_type','main_material']


class ProjectImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify projects' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":5,
     "image": "project_image_url",
     "project":project_id
     }
     Use other functions by accessing this url:
     project/projectImage/<project's_id>
     Format of data will be as the previous data format for GET function
     To Get All Project's Images use this url:
     project/projectImage/?project=<project's_id>
    """

    def get_view_name(self):
        return _("Create/Modify Project Images")

    from .serializers import ProjectImageSerializer
    serializer_class = ProjectImageSerializer
    from .models import ProjectImages
    permission_classes = [UnisealPermission]
    queryset = ProjectImages.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']


class ProjectVideoViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify project' videos by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id":7,
         "video": "project_video_url",
         "project":project_id
         }
         Use other functions by accessing this url:
         project/projectVideo/<projectVideo's_id>
         Format of data will be as the previous data format for GET function
         To Get All Project's Videos use this url:
         project/projectVideo/?project=<project's_id>

        """

    def get_view_name(self):
        return _("Create/Modify Projects Videos")

    from .serializers import ProjectVideoSerializer
    serializer_class = ProjectVideoSerializer
    from .models import ProjectVideos
    permission_classes = [UnisealPermission]
    queryset = ProjectVideos.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

class ProjectSolutionViewSet(viewsets.ModelViewSet):
    """API endpoint to add solutions to projects by admin
        this endpoint allows GET,PUT,PATCH,DELETE functions
        permissions to this view is restricted as the following:
        - Only admin users can use all functions on this endpoint
        - Registered users are only allowed to use GET function
        Data will be retrieved in the following format for GET function:
        {
         "id": 9,
         "project":project_id,
         "solution":solution_id,
         }
         Use other functions by accessing this url:
         project/projectSolution/<projectSolution's_id>
         Format of data will be as the previous data format for GET function
         To Get All projects that have used the same solution use this url:
         project/projectSolution/?solution=<solution_id>
         To Get All solutions that have been used in the same project :
         project/projectSolution/?project=<project_id>
        """

    def get_view_name(self):
        return _("Add/Remove Projects Solutions")

    from .serializers import ProjectSolutionSerializer
    serializer_class = ProjectSolutionSerializer
    from .models import ProjectSolutions
    permission_classes = [UnisealPermission]
    queryset = ProjectSolutions.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project','solution']

#Views for dashboard
searchManObj = SearchMan("Project")
report_man = ReportMan()
# report_man.setTempDir(tempfile.mkdtemp())
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    project_name = []
    beneficiary = []
    description = []
    main_material = []
    project_type = []
    execution_date = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Project Name":
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        project_name.append(project.name)
            elif header == "Beneficiary":
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        beneficiary.append(project.beneficiary)
            elif header == "Description":
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        description.append(project.description)
            elif header == "Main Material Used":
                print("here in supplier selected")
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        main_material.append(project.main_material)
            elif header == "Project Type":
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        project_type.append(project.project_type.name)
            elif header == "Execution Date":
                for page in selected_pages:
                    for project in paginator_obj.page(page):
                        execution_date.append(project.date)
    else:
        headers_here = ["Project Name", "Beneficiary","Description", "Main Material Used", "Project Type", "Execution Date"]
        for page in range(1, paginator_obj.num_pages+1):
            for project in paginator_obj.page(page):
                project_name.append(project.name)
                beneficiary.append(project.beneficiary)
                description.append(project.description)
                main_material.append(project.main_material)
                project_type.append(project.project_type.name)
                execution_date.append(project.date)
    return headers_here, project_name,  beneficiary, description,main_material, project_type,execution_date

def prepare_query(paginator_obj,headers=None):
    project_name = []
    beneficiary = []
    description = []
    main_material = []
    project_type = []
    execution_date = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Project Name":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        project_name.append(project.name)
            elif header == "Beneficiary":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        beneficiary.append(project.beneficiary)
            elif header == "Description":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        description.append(project.description)
            elif header == "Main Material Used":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        main_material.append(project.main_material)
            elif header == "Project Type":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        project_type.append(project.project_type.name)
            elif header == "Execution Date":
                for page in range(1, paginator_obj.num_pages+1):
                    for project in paginator_obj.page(page):
                        execution_date.append(project.date)
    else:
        headers_here = ["Project Name","Beneficiary","Description","Main Material Used","Project Type","Execution Date"]
        for page in range(1, paginator_obj.num_pages+1):
            for project in paginator_obj.page(page):
                project_name.append(project.name)
                beneficiary.append(project.beneficiary)
                description.append(project.description)
                main_material.append(project.main_material)
                project_type.append(project.project_type.name)
                execution_date.append(project.date)

    # later for extracting actual data


    return headers_here,project_name,beneficiary,description,main_material,project_type,execution_date

@login_required(login_url='login')
def all_projects(request):
    from project.models import Project
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
      PROJECT_NAME_SYNTAX_ERROR,
    PROJECT_TYPE_SYNTAX_ERROR,
    BENEFICIARY_NAME_SYNTAX_ERROR,
    MAIN_MATERIAL_SYNTAX_ERROR,
    EXECUTION_DATE_ERROR,
    PROJECT_NOT_FOUND

    )
    search_result = ''
    all_projects = Project.objects.all().order_by("id")
    paginator = Paginator(all_projects, 5)

    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'project':
            search_message = request.POST.get('search_phrase')
            search_result = Project.objects.filter(name__icontains=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Project Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'beneficiary':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(beneficiary__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Beneficiary Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'main_material':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(main_material__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Main Material Used:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(project_type__name__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Project Type:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'execution_year':
            search_phrase = request.POST.get('search_phrase_date')
            search_result = Project.objects.filter(date__contains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Execution Year')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Project Name") if request.POST.get('project_name_header') is not None else ''
        headers.append("Beneficiary") if request.POST.get('beneficiary_header') is not None else ''
        headers.append("Description") if request.POST.get('description_header') is not None else ''
        headers.append("Main Material Used") if request.POST.get('main_material_header') is not None else ''
        headers.append("Project Type") if request.POST.get('project_type_header') is not None else ''
        headers.append("Execution Date") if request.POST.get('execution_date_header') is not None else ''
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
                constructor = {}
                headers,project_name,beneficiary,description,main_material,project_type,execution_date = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(project_name) > 0:
                    constructor.update({"project_name": project_name})
                if len(beneficiary) > 0:
                    constructor.update({"beneficiary": beneficiary})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(main_material) > 0:
                    constructor.update({"main_material": main_material})
                if len(project_type) > 0:
                    constructor.update({"project_type": project_type})
                if len(execution_date) > 0:
                    constructor.update({"execution_date": execution_date})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Projects',
                                                                                  headers,request=request, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    # messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Project Name", "Beneficiary", "Description", "Main Material Used", "Project Type",
                                "Execution Date"]

                headers,project_name,beneficiary,description,main_material,project_type,execution_date = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Projects',
                                                                                  headers,request=request, project_name=project_name,
                                                                                  beneficiary=beneficiary,
                                                                                  description=description,
                                                                                  main_material=main_material,
                                                                                  project_type=project_type,
                                                                                  execution_date = execution_date
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    # messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            query = searchManObj.getPaginator()
            if len(headers) > 0:
                constructor = {}
                headers, project_name, beneficiary, description, main_material, project_type, execution_date = prepare_query( paginator_obj=query,
                    headers=headers)
                if len(project_name) > 0:
                    constructor.update({"project_name": project_name})
                if len(beneficiary) > 0:
                    constructor.update({"beneficiary": beneficiary})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(main_material) > 0:
                    constructor.update({"main_material": main_material})
                if len(project_type) > 0:
                    constructor.update({"project_type": project_type})
                if len(execution_date) > 0:
                    constructor.update({"execution_date": execution_date})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Projects',
                                                                                  headers,request=request, **constructor)
                if status:
                   request.session['temp_dir'] = 'delete baby!'

                   # messages.success(request, f"Report Successfully Created ")
                   # return redirect('download_file',filepath=filepath,filename=filename)

                   return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers,project_name,beneficiary,description,main_material,project_type,execution_date = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Projects',
                                                                                  headers,request=request, project_name=project_name,
                                                                                  beneficiary=beneficiary,
                                                                                  description=description,
                                                                                  main_material=main_material,
                                                                                  project_type=project_type,
                                                                                  execution_date=execution_date,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    # messages.success(request, f"Report Successfully Created")
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
        projects = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        projects = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        projects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'project/all_projects.html',
                  {
                      'title': _('All Projects'),
                      'all_projects': 'active',
                      'all_projects_data': projects,
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
                          "project_error": PROJECT_NAME_SYNTAX_ERROR,
                          "beneficiary_error": BENEFICIARY_NAME_SYNTAX_ERROR,
                          "main_material_error": MAIN_MATERIAL_SYNTAX_ERROR,
                          "type_error":PROJECT_TYPE_SYNTAX_ERROR,
                          "execution_date_error":EXECUTION_DATE_ERROR,
                      },
                      'not_found':PROJECT_NOT_FOUND,
                  }
                  )
@login_required(login_url='login')
def add_projects(request):
    from .forms import ProjectForm
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            # project.execution_date = request.POST['execution_date']
            project.save()
            project.slug = slugify(rand_slug())
            project.save()
            project_name = form.cleaned_data.get('name')
            messages.success(request, f"New Project Added: {project_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = ProjectForm()
    context = {
        'title': _('Add Projects'),
        'add_projects': 'active',
        'form':form,
    }
    return render(request, 'project/add_projects.html', context)
@login_required(login_url='login')
def delete_projects(request):
    from project.models import Project
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    all_projects = Project.objects.all().order_by("id")
    paginator = Paginator(all_projects, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PROJECT_NAME_SYNTAX_ERROR,
        PROJECT_TYPE_SYNTAX_ERROR,
        BENEFICIARY_NAME_SYNTAX_ERROR,
        MAIN_MATERIAL_SYNTAX_ERROR,
        EXECUTION_DATE_ERROR,
        PROJECT_NOT_FOUND


    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        print("first")
        if request.POST.get('search_options') == 'project':
            search_message = request.POST.get('search_phrase')
            search_result = Project.objects.filter(name__icontains=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Project Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'beneficiary':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(beneficiary__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Beneficiary Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'main_material':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(main_material__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Main Material Used:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(project_type__name__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Project Type:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'execution_year':
            search_phrase = request.POST.get('search_phrase_date')
            search_result = Project.objects.filter(date__contains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Execution Year')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        print("second")
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        print("third")
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)

    if request.GET.get('page'):
        print("fourth")
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        projects = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        projects = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        projects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'project/delete_projects.html',
                  {
                      'title': _('Delete Projects'),
                      'delete_projects': 'active',
                      'all_projects_data': projects,
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
                          "project_error": PROJECT_NAME_SYNTAX_ERROR,
                          "beneficiary_error": BENEFICIARY_NAME_SYNTAX_ERROR,
                          "main_material_error": MAIN_MATERIAL_SYNTAX_ERROR,
                          "type_error": PROJECT_TYPE_SYNTAX_ERROR,
                          "execution_date_error": EXECUTION_DATE_ERROR,
                      },
                      'not_found': PROJECT_NOT_FOUND,
                  }
                  )
@login_required(login_url='login')
def edit_projects(request):
    from project.models import Project
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
      PROJECT_NAME_SYNTAX_ERROR,
    PROJECT_TYPE_SYNTAX_ERROR,
    BENEFICIARY_NAME_SYNTAX_ERROR,
    MAIN_MATERIAL_SYNTAX_ERROR,
    EXECUTION_DATE_ERROR,
    PROJECT_NOT_FOUND

    )
    search_result = ''
    all_projects = Project.objects.all().order_by("id")
    paginator = Paginator(all_projects, 5)
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'project':
            search_message = request.POST.get('search_phrase')
            search_result = Project.objects.filter(name__icontains=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Project Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'beneficiary':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(beneficiary__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Beneficiary Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'main_material':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(main_material__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Main Material Used:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'type':
            search_phrase = request.POST.get('search_phrase')
            search_result = Project.objects.filter(project_type__name__icontains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Project Type:')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'execution_year':
            search_phrase = request.POST.get('search_phrase_date')
            search_result = Project.objects.filter(date__contains=search_phrase).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Execution Year')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_projects = Project.objects.all().order_by("id")
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        projects = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        projects = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        projects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'project/edit_projects.html',
                  {
                      'title': _('Edit Projects'),
                      'edit_projects': 'active',
                      'all_projects_data': projects,
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
                          "project_error": PROJECT_NAME_SYNTAX_ERROR,
                          "beneficiary_error": BENEFICIARY_NAME_SYNTAX_ERROR,
                          "main_material_error": MAIN_MATERIAL_SYNTAX_ERROR,
                          "type_error": PROJECT_TYPE_SYNTAX_ERROR,
                          "execution_date_error": EXECUTION_DATE_ERROR,
                      },
                      'not_found': PROJECT_NOT_FOUND,
                  }
                  )
@login_required(login_url='login')
def project_details(request,slug):
    from project.models import Project,ProjectImages
    # from .forms import ProductForm
    # all_products = Product.objects.all().order_by("id")
    # paginator = Paginator(all_products, 5)
    # fetch the object related to passed id
    project = get_object_or_404(Project, slug=slug)
    projectImages = ProjectImages.objects.filter(project__slug=slug)
    pureImages = list()
    if projectImages :
        pureImages.append(project.image.url)
        for image in projectImages:
            pureImages.append(image.image.url)

    if request.method == "GET":
        if projectImages :
            print("its noot empty yo!")
            print(project.image.url)
        else:
            print("its emmpty yoooo!")



    return render(request, 'project/project_detail.html',
                  {
                      'title': _('Project Details'),
                      'all_projects': 'active',
                      'project_data': project,
                      'project_images':pureImages,
                      'project_original_image':project.image.url


                  }
                  )
@login_required(login_url='login')
def project_images(request,slug=None):
    import os
    from project.models import Project,ProjectImages
    from .forms import ProjectImagesForm
    allProjects = Project.objects.all()

    pureImages = {}
    context = {
        'title': _('Project Images'),
        'project_images_base': 'active',
        'allProjects': allProjects,
    }
    if slug != None and request.method =='GET':
        print("slug is not null")

        project = get_object_or_404(Project, slug=slug)
        projectImages = ProjectImages.objects.filter(project__slug=slug)
        if projectImages:
            # pureImages.append(project.image.url)
            pureImages.update({True: project.image.url})
            for image in projectImages:
                # pureImages.append(image.image.url)
                pureImages.update({image.image.url: image.image.url})
        print(pureImages)
        context =  {
            'title': _('Project Images'),
            'all_projects': 'active',
            'project_data': project,
            'project_images': pureImages,
            'project_original_image': project.image.url,

            'allProjects': allProjects,
            'slug':slug
        }
        form = ProjectImagesForm()
        context.update({"form": form})


    if request.method == 'POST' and 'search_project' in request.POST:
        if request.POST.get('search_options') != 'none':
            print("searching for a project")
            chosen_project = request.POST.get('search_options')

            return redirect('projectImages', slug=chosen_project)
        else:
            messages.error(request, "Please choose a project from the list")




    if request.method == 'POST' and 'add_images' in request.POST:
        print("adding new images")
        form = ProjectImagesForm(request.POST, request.FILES)
        project = get_object_or_404(Project, slug=slug)
        selected_project = Project.objects.filter(slug=slug)
        files = request.FILES.getlist('image')
        form.project = selected_project
        if form.is_valid():
            if len(files) == 1:
                print("there is more than images")

                updated_project = form.save(commit=False)
                updated_project.image = request.FILES['image']
                # updated_project.project = selected_project.id
                updated_project.slug = slugify(rand_slug())
                # updated_project.save()
                project_name = project.name
                messages.success(request, f"New image Added for: {project_name}")

            else:
                for f in files:
                    ProjectImages.objects.create(project=project, image=f)
                project_name = project.name
                messages.success(request, f"New images Added for: {project_name}")
            return redirect('projectImages', slug=slug)
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    if request.method == 'POST' and 'confirm_changes' in request.POST:
        project_instances = ProjectImages.objects.annotate(num_projects=Count('project')).filter(project__slug=slug)
        all_project_images_count = project_instances.count()+1
        print("total images count for selected project: ",all_project_images_count)
        default_image = request.POST.get('posted_default_image')
        deleted_images = request.POST.get('posted_deleted_images')
        print("default image is: ",default_image)
        # handling default image first
        current_project = Project.objects.get(slug=slug)
        current_default_image = current_project.image
        if default_image != 'none':
            if current_default_image != default_image:
                default_image_path = default_image
                just_image_path = default_image_path.split('/media')
                Project.objects.filter(slug=slug).update(image=just_image_path[1])
                ProjectImages.objects.create(project=current_project, image=just_image_path[1])

        if deleted_images != 'none':
            # check that the selected images are not greater than all of the project's images
            print("deleted images are: ", deleted_images.split(','))
            print("now deleting images ")
            for instance in project_instances:
                for image in deleted_images.split(','):
                    if instance.image.url == image:
                        deleted_image_path = os.path.dirname(os.path.abspath('unisealAPI'))+image
                        deleted_record = ProjectImages.objects.get(id=instance.id)
                        print("deleted image path: ",image)
                        deleted_record.delete()
                        if os.path.exists(deleted_image_path):
                            os.remove(deleted_image_path)
        messages.success(request,f"Project {current_project.name} was successfully updated!")
        return redirect('projectImages', slug=slug)


    return render(request, 'project/project_images.html',
                 context

                  )

@login_required(login_url='login')
def edit_project(request,slug):
    from project.models import Project
    from .forms import ProjectForm,ProjectImagesForm
    obj = get_object_or_404(Project, slug=slug)
    project_form = ProjectForm(request.POST or None, instance=obj)
    project_image_form = ProjectImagesForm(request.POST or None, instance=obj)
    if project_form.is_valid():
        if request.FILES:
            project = project_form.save()
            project.image = request.FILES['image']
            project.save()
        project_form.save()
        project_name = project_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {project_name} Data")
    else:
        for field, items in project_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Project'),
        'edit_projects': 'active',
        'project':obj,
        'form':project_form,
        'all_projects': all_projects,
        'project_form': project_form,
        'project_image_form': project_image_form
    }
    return render(request, 'project/edit_project.html', context)
@login_required(login_url='login')
def confirm_delete(request,id):
    import os
    from project.models import Project
    obj = get_object_or_404(Project, id=id)
    try:
        deleted_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + obj.image.url
        print("deleted image path: ",deleted_image_path)
        if os.path.exists(deleted_image_path):
            os.remove(deleted_image_path)
        obj.delete()

        messages.success(request, f"Project << {obj.name} >> deleted successfully")
    except:
        messages.error(request, f"Project << {obj.name} >> was not deleted , please try again!")


    return redirect('deleteProjects')
