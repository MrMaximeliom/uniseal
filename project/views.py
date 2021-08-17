from django.template.defaultfilters import slugify

from Util.permissions import UnisealPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from  django.contrib import messages
from django.contrib.auth.decorators import login_required

from Util.utils import rand_slug


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
     "title":"project_title",
     "category":"project_category",
     "beneficiary":"beneficiary_name",
     "image":"project_image_url",
     "description":"project_description",
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


@login_required(login_url='login')
def all_projects(request):
    from project.models import Project
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    all_projects = Project.objects.all().order_by("id")
    paginator = Paginator(all_projects, 5)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
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
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def add_projects(request):
    from .forms import ProjectForm
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.execution_date = request.POST['execution_date']
            project.save()
            project.slug = slugify(rand_slug())
            project.save()
            project_name = form.cleaned_data.get('name')
            messages.success(request, f"New User Added: {project_name}")
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

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
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
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_projects(request):
    from project.models import Project
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    all_projects = Project.objects.all().order_by("id")
    paginator = Paginator(all_projects, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
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
                      'current_page': page
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
def project_images(request,slug):
    from project.models import Project,ProjectImages
    from .forms import ProjectImagesForm
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

    if request.method == 'POST':
        form = ProjectImagesForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = ProjectImagesForm()



    return render(request, 'project/project_images.html',
                  {
                      'title': _('Project Images'),
                      'all_projects': 'active',
                      'project_data': project,
                      'project_images':pureImages,
                      'project_original_image':project.image.url,
                      'form':form
                  })

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
        'all_products': all_projects,
        'project_form': project_form,
        'project_image_form': project_image_form
    }
    return render(request, 'project/edit_project.html', context)
@login_required(login_url='login')
def confirm_delete(request,id):
    from project.models import Project
    obj = get_object_or_404(Project, id=id)
    try:
        obj.delete()
        messages.success(request, f"Project {obj.name} deleted successfully")
    except:
        messages.error(request, f"Project {obj.name} was not deleted , please try again!")


    return redirect('deleteProjects')
