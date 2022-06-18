from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from Util.utils import SearchMan, ReportMan, delete_temp_folder
from Util.utils import rand_slug

searchManObj = SearchMan("Project")
report_man = ReportMan()

# new code starts here
from apps.common_code.views import BaseListView
from apps.project.models import Project


class ProjectListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            }
        }
        return super().get(request)

    def post(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'project':
                search_message = request.POST.get('search_phrase')
                search_result = Project.objects.filter(name__icontains=search_message).order_by("id")
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

        if request.POST.get('clear') == 'clear':
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1

        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,

            }
        }
        return super().get(request)


# ends here



@staff_member_required(login_url='login')
def project_details(request, slug):
    from apps.project.models import Project, ProjectImages
    project = get_object_or_404(Project, slug=slug)
    projectImages = ProjectImages.objects.filter(project__slug=slug)
    pureImages = list()
    if projectImages:
        pureImages.append(project.image.url)
        for image in projectImages:
            pureImages.append(image.image.url)

    if request.method == "GET":
        if projectImages:
            print("its noot empty yo!")
            print(project.image.url)
        else:
            print("its emmpty yoooo!")

    return render(request, 'project/project_detail.html',
                  {
                      'title': _('Project Details'),
                      'all_projects': 'active',
                      'project_data': project,
                      'projects': 'active',
                      'project_images': pureImages,
                      'project_original_image': project.image.url

                  }
                  )

@staff_member_required(login_url='login')
def project_images(request, slug=None):
    import os
    from apps.project.models import Project, ProjectImages
    from .forms import ProjectImagesForm
    allProjects = Project.objects.all()

    pureImages = {}
    context = {
        'title': _('Project Images'),
        'project_images_base': 'active',
        'allProjects': allProjects,
        'projects': 'active',
    }
    if slug != None and request.method == 'GET':
        project = get_object_or_404(Project, slug=slug)
        projectImages = ProjectImages.objects.filter(project__slug=slug)
        if projectImages:
            # pureImages.append(project.image.url)
            pureImages.update({True: project.image.url})
            for image in projectImages:
                # pureImages.append(image.image.url)
                pureImages.update({image.image.url: image.image.url})
        # print("default image is: \n",default_project_image.image.url)
        context = {
            'title': _('Project Images'),
            'all_projects': 'active',
            'project_data': project,
            'projects': 'active',
            'project_images': pureImages,
            'project_original_image': project.image,

            'allProjects': allProjects,
            'slug': slug
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
        form = ProjectImagesForm(request.POST, request.FILES)
        project = get_object_or_404(Project, slug=slug)
        selected_project = Project.objects.filter(slug=slug)
        files = request.FILES.getlist('image')
        form.project = selected_project
        if form.is_valid():
            if len(files) == 1:
                updated_project = form.save(commit=False)
                updated_project.image = request.FILES['image']
                updated_project.slug = slugify(rand_slug())
                # updated_project.save()
                project_name = project.name
                messages.success(request, f"New image Added for: {project_name}")

            else:
                projectImagesList = list()
                for f in files:
                    # ProjectImages.objects.create(project=project, image=f)
                    projectImagesList.append(ProjectImages(project=project, image=f))
                ProjectImages.objects.bulk_create(projectImagesList)
                project_name = project.name
                messages.success(request, f"New images Added for: {project_name}")
            return redirect('projectImages', slug=slug)
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    if request.method == 'POST' and 'confirm_changes' in request.POST:
        project_instances = ProjectImages.objects.annotate(num_projects=Count('project')).filter(project__slug=slug)
        all_project_images_count = project_instances.count() + 1
        print("total images count for selected project: ", all_project_images_count)
        default_image = request.POST.get('posted_default_image')
        deleted_images = request.POST.get('posted_deleted_images')
        print("default image is: ", default_image)
        # handling default image first
        current_project = Project.objects.get(slug=slug)
        current_default_image = current_project.image
        if default_image != 'none':
            if current_default_image != default_image:
                default_image_path = default_image
                just_image_path = default_image_path.split('/media')
                image_path_for_previous_default_image = current_default_image
                modified_image_path =default_image_path.split('/media/')
                # moving previous default image to be in the place of other image
                ProjectImages.objects.filter(project=current_project, image=modified_image_path[1]).update(
                    image=image_path_for_previous_default_image)
                # # check for existence of the replaced default image path and then remove it from OS
                # replaced_default_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + default_image_path
                # if os.path.exists(replaced_default_image_path):
                #     os.remove(replaced_default_image_path)
                # # making selected image as default image
                Project.objects.filter(slug=slug).update(image=just_image_path[1])
                # check for existence of default image and the remove it form OS
                # previous_default_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + current_project.image.url
                # if os.path.exists(previous_default_image_path):
                #     os.remove(previous_default_image_path)

                print("chosen default image path is: ",default_image_path)
                print("other image path is: ",image_path_for_previous_default_image)



        if len(deleted_images) != 0:
            # check that the selected images are not greater than all of the project's images
            print("deleted images are: ", deleted_images.split(','))
            print("now deleting images ")
            for instance in project_instances:
                for image in deleted_images.split(','):
                    if instance.image.url == image:
                        deleted_image_path = os.path.dirname(os.path.abspath('unisealAPI')) + image
                        deleted_record = ProjectImages.objects.get(id=instance.id)
                        print("deleted image path: ", image)
                        deleted_record.delete()
                        if os.path.exists(deleted_image_path):
                            os.remove(deleted_image_path)
        messages.success(request, f"Project {current_project.name} was successfully updated!")
        return redirect('projectImages', slug=slug)

    return render(request, 'project/project_images.html',
                  context

                  )

class TopProjectsHelper:
    query = ''
    def setQuery(self, query):
        self.query = query

    def getQuery(self):
        return self.query

top_projects_helper = TopProjectsHelper()
@staff_member_required(login_url='login')
def top_projects(request):
    from apps.project.models import Project
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PROJECT_NAME_SYNTAX_ERROR,
        BENEFICIARY_NAME_SYNTAX_ERROR,
    MAIN_MATERIAL_SYNTAX_ERROR,
        PROJECT_NOT_FOUND,
    PROJECT_TYPE_SYNTAX_ERROR,
    EXECUTION_DATE_ERROR,
    CLEAR_SEARCH_TIP,
    CREATE_REPORT_TIP,
    SEARCH_PROJECTS_TIP,

    )
    all_projects = Project.objects.filter(is_top=True)
    top_projects_helper.setQuery(all_projects)
    search_result = ''
    displaying_type = 'Top Projects'
    if request.method == "POST" and 'clear' not in request.POST  and 'updating_top_projects' not in request.POST :
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'project':
            search_message = request.POST.get('search_phrase')
            search_message = search_message.strip(' ')
            search_result = Project.objects.filter(name__icontains=search_message)
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Project Name: ')
            searchManObj.setSearchError(False)
            top_projects_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'beneficiary':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_phrase = search_phrase.strip(' ')
            search_result = Project.objects.filter(beneficiary__icontains=search_phrase)
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Beneficiary: ')
            searchManObj.setSearchError(False)
            top_projects_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'main_material':
            search_phrase = request.POST.get('search_phrase')
            search_phrase = search_phrase.strip(' ')
            print('search phrase is ', search_phrase)
            search_result = Project.objects.filter(main_material__icontains=search_phrase)
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Main Material: ')
            searchManObj.setSearchError(False)
            top_projects_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'type':
            search_phrase = request.POST.get('search_phrase')
            search_phrase = search_phrase.strip(' ')
            search_result = Project.objects.filter(project__is_top=True,project_type__icontains=search_phrase)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Project Type: ')
            searchManObj.setSearchError(False)
            top_projects_helper.setQuery(search_result)
        elif request.POST.get('search_options') == 'top_projects':
            search_phrase = request.POST.get('search_phrase')
            search_phrase = search_phrase.strip(' ')
            search_result = Project.objects.filter(is_top=True,name__icontains=search_phrase)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Top Projects: ')
            searchManObj.setSearchError(False)
            top_projects_helper.setQuery(search_result)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        print("iam here now")
        all_projects = Project.objects.filter(is_top=True)
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
        top_projects_helper.setQuery(all_projects)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_projects = Project.objects.filter(is_top=True)
        searchManObj.setPaginator(all_projects)
        searchManObj.setSearch(False)
        top_projects_helper.setQuery(all_projects)
    if request.method == 'POST' and 'updating_top_projects' in request.POST:
        print("Oi man iam updating your top projects yo!!")
        searchManObj.setSearch(False)
        selected_top_projects = request.POST.get('selected_top_projects')
        deleted_top_projects = request.POST.get('deleted_top_projects')
        print("selected projects are: ",selected_top_projects)
        print("deleted top projects are: ",deleted_top_projects)
        updated = False
        if selected_top_projects != 'none':
            selected_projects = list()
            # selected_products_ids = request.POST.get('selected_top_products')
            print("top projects are: ",selected_top_projects)
            print("\ntop projects splited: ",selected_top_projects.split(','))
            print("\n cycling throw splited projects")
            for project_id in selected_top_projects.split(','):
                print(project_id)
            from apps.project.models import Project
            for project_id in selected_top_projects.split(','):
                selected_projects.append(
                    Project.objects.get(id=project_id)
                )
            print("selected products are: \n")
            print(selected_projects)
            for project in selected_projects:
                project.is_top = True
            Project.objects.bulk_update(selected_projects, ['is_top'])
        if deleted_top_projects != 'none':
            deleted_projects = list()
            # selected_products_ids = request.POST.get('selected_top_products')
            print("deleted top projects are: ",deleted_top_projects)
            print("\ndeleted top projects splited: ",deleted_top_projects.split(','))
            print("\n cycling throw splited projects")
            for project_id in deleted_top_projects.split(','):
                print(project_id)
            from apps.project.models import Project
            for project_id in deleted_top_projects.split(','):
                deleted_projects.append(
                    Project.objects.get(id=project_id)
                )
            print("selected projects are: \n")
            print(deleted_projects)
            for project in deleted_projects:
                project.is_top = False
            Project.objects.bulk_update(deleted_projects, ['is_top'])
        if updated:
            messages.success(request,"Top Projects Updated Successfully!")

    return render(request, 'project/top_projects.html',
                  {
                      'title': _('Top Projects'),
                      'top_projects': 'active',
                      'projects': 'active',
                      'all_projects_data': top_projects_helper.getQuery(),
                      'displaying_type': displaying_type,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'create_report_tip':CREATE_REPORT_TIP,
                      'clear_search_tip':CLEAR_SEARCH_TIP,
                      'search_projects_tip':SEARCH_PROJECTS_TIP,
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
