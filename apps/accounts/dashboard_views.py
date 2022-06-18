from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.generic import ListView
from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder, \
    check_phone_number,prepare_selected_query,prepare_default_query,\
    get_selected_pages,get_fields_names_for_report_file



searchManObj = SearchMan("User")
report_man = ReportMan()

"""
UsersListView Model:
is a subclass from the class ListView which is used to list
all users of the User model
it requires to define the following params:
- model (the model of the updated instance)
- template_name ( the path of the view that will be used)
- active_flag (this flag is used to add 'active' class to the current pages in sidebar) 
- main_active_flag (this flag is used to add 'active' class to the main master current pages in sidebar) 
- model_name (this variable is used to specify model name for SearchMan class) 
- title (specifies the page's title)
"""
class UsersListView(ListView):
    model = None
    template_name = None
    main_active_flag = None
    active_flag = None
    model_name = None
    title = None
    searchManObj = SearchMan(model_name)
    # return default queryset used in this view
    def get_queryset(self):
        from apps.accounts.models import User
        return User.objects.all().order_by('-id')
    # post method used in HTTP POST call
    def post(self,request,*args,**kwargs):
        from apps.accounts.models import User
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            USERNAME_SYNTAX_ERROR,
            FULL_NAME_SYNTAX_ERROR,
            ORGANIZATION_NAME_SYNTAX_ERROR,
            PHONE_NUMBER_SYNTAX_ERROR,
            SEARCH_USERS_TIP,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP
        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        # check if it's a search request using POST method
        if  'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            # check if searched phrased matches one of the columns' names
            if request.POST.get('search_options') == 'full_name':
                # get search phrase
                search_message = request.POST.get('search_phrase')
                # search by the search phrase and column name
                search_result = User.objects.filter(full_name=search_message).order_by("id")
                # set paginator object with search result
                searchManObj.setPaginator(search_result)
                # set search phrase message
                searchManObj.setSearchPhrase(search_message)
                # set search option
                searchManObj.setSearchOption('Full Name')
                # set search error to => False
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'username':
                print('here now in username')
                search_phrase = request.POST.get('search_phrase')
                search_result = User.objects.filter(username=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Username')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'organization':
                search_phrase = request.POST.get('search_phrase')
                search_result = User.objects.filter(organization=search_phrase).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Organization')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'phone_number':
                print('here now in phone number')
                search_phrase = request.POST.get('search_phrase')
                is_number_ok, phone_number = check_phone_number(search_phrase)
                if (is_number_ok):
                    search_result = User.objects.filter(phone_number=phone_number).order_by("id")
                    searchManObj.setPaginator(search_result)
                    searchManObj.setSearchPhrase(search_phrase)
                    searchManObj.setSearchOption('Phone Number')
                    searchManObj.setSearchError(False)
            else:
                # display error message if something goes wrong
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")
                searchManObj.setSearchError(True)
        # check if it's a clear request using POST method
        if  request.POST.get('clear') == 'clear':
            # get all users
            all_users = User.objects.all().order_by("id")
            # set paginator with all users
            searchManObj.setPaginator(all_users)
            # set search to => False
            searchManObj.setSearch(False)
        # check if it's a creation for Excel file
        if request.POST.get('createExcel') == 'done':
            # define headers of the Excel file
            headers = []
            # check selected fields by the user for the creation of the report Excel file
            headers.append("full_name") if request.POST.get('full_name_header') is not None else ''
            headers.append("username") if request.POST.get('username_header') is not None else ''
            headers.append("organization") if request.POST.get('organization_header') is not None else ''
            headers.append("job_type") if request.POST.get('job_type_header') is not None else ''
            headers.append("phone_number") if request.POST.get('phone_number_header') is not None else ''
            headers.append("last_login") if request.POST.get('last_login_header') is not None else ''
            # check if user selected pages to create the report Excel file
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = searchManObj.getPaginator()
                # check if headers length is greater than 0
                if len(headers) > 0:
                    # create a dictionary contains columns' names and their values
                    # from the query and the selected headers and using paginator object
                    constructor = prepare_selected_query(searchManObj.get_queryset(), headers, selected_pages, query)
                    # get status of the creation process for the report file
                    # set the file path and file name for the ReportMan's object attributes
                    # by calling the function createExcelFile and pass file name , headers , and de structured constructor variable
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                      **constructor)
                    # check if the file Excel file created successfully or not
                    if status:
                        # set session variable temp_dir to value => delete man
                        request.session['temp_dir'] = 'delete man!'
                        # send success message of creating the report Excel file
                        messages.success(request, f"Report Successfully Created ")
                        # re orient the call to the URL to download the created report Excel file
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        # send error message if the file creation process was broken
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
                else:
                    print("here ya dody")
                    # set default headers if the user has not selected any
                    headers = get_fields_names_for_report_file(User,User.get_not_wanted_fields_names_in_report_file())
                    # create a dictionary contains columns' names and their values
                    # from the User model and the default headers and using paginator object
                    constructor = prepare_selected_query(searchManObj.get_queryset(),headers,
                        selected_pages, query)
                    # get status of the creation process for the report file
                    # set the file path and file name for the ReportMan's object attributes
                    # by calling the function createExcelFile and pass file name , headers , and de structured constructor variable
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                    **constructor)
                    # check if the file Excel file created successfully or not
                    if status:
                        # set session variable temp_dir to value => delete man
                        request.session['temp_dir'] = 'delete man!'
                        # send success message of creating the report Excel file
                        messages.success(request, f"Report Successfully Created ")
                        # re orient the call to the URL to download the created report Excel file
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        # send error message if the file creation process was broken
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            else:
                # get the original query of page and then structure the data
                query = searchManObj.getPaginator()
                # set default headers if the user has not selected any
                # headers = get_fields_names_for_report_file(User, User.get_not_wanted_fields_names_in_report_file())
                if len(headers) > 0:
                    constructor = prepare_default_query(
                        searchManObj.get_queryset(),
                        headers,
                        query)
                    # get status of the creation process for the report file
                    # set the file path and file name for the ReportMan's object attributes
                    # by calling the function createExcelFile and pass file name , headers , and de structured constructor variable
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                      **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")

                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    print("pages are not selected")

                    constructor = prepare_default_query(searchManObj.get_queryset(),
                        headers,query)
                    # get status of the creation process for the report file
                    # set the file path and file name for the ReportMan's object attributes
                    # by calling the function createExcelFile and pass file name , headers , and de structured constructor variable
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                      **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))


                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

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
                'user_data': User.objects.filter(username=self.request.user.username),
                self.main_active_flag: 'active',
                self.active_flag: "active",
                "instances_count": len(self.get_queryset()),
                'current_page': page,
                'title': self.title,
                'all_users_data': instances,
                'search': searchManObj.getSearch(),
                'search_result': search_result,
                'search_phrase': searchManObj.getSearchPhrase(),
                'search_option': searchManObj.getSearchOption(),
                'search_error': searchManObj.getSearchError(),
                'create_report_tip': CREATE_REPORT_TIP,
                'clear_search_tip': CLEAR_SEARCH_TIP,
                'search_users_tip': SEARCH_USERS_TIP,
                'data_js': {
                    "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                    "username_error": USERNAME_SYNTAX_ERROR,
                    "organization_error": ORGANIZATION_NAME_SYNTAX_ERROR,
                    "full_name_error": FULL_NAME_SYNTAX_ERROR,
                    "phone_number_error": PHONE_NUMBER_SYNTAX_ERROR
                }
            }
        return super().get(request)

    def get(self, request, *args, **kwargs):
        from apps.accounts.models import User
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            USERNAME_SYNTAX_ERROR,
            FULL_NAME_SYNTAX_ERROR,
            ORGANIZATION_NAME_SYNTAX_ERROR,
            PHONE_NUMBER_SYNTAX_ERROR,
            SEARCH_USERS_TIP,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session :
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = self.model.objects.all().order_by('-id')
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
            'user_data': User.objects.filter(username=self.request.user.username),
            self.main_active_flag: 'active',
            self.active_flag: "active",
            "instances_count": len(self.get_queryset()),
            'current_page': page,
            'title': self.title,
            'all_users_data': instances,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_users_tip': SEARCH_USERS_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                "username_error": USERNAME_SYNTAX_ERROR,
                "organization_error": ORGANIZATION_NAME_SYNTAX_ERROR,
                "full_name_error": FULL_NAME_SYNTAX_ERROR,
                "phone_number_error": PHONE_NUMBER_SYNTAX_ERROR
            }
        }
        return super().get(request)
"""
change_password function:
is a method used to change a user's password
"""

@staff_member_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        # get the user's data from the form
        form = PasswordChangeForm(request.user, request.POST)
        # check if user's data is valid
        if form.is_valid():
            # save data
            user = form.save()
            # update session authentication hash
            update_session_auth_hash(request, user)
            # send a success message to the user
            messages.success(request, 'Your password was successfully updated!')
            # return to the changePassword route after submitting the form
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # if the request method is GET , initiate the form object
        form = PasswordChangeForm(request.user)
    # render the change_password html page to the user , add the form object to the render method
    return render(request, 'accounts/change_password.html', {
        'form': form
    })