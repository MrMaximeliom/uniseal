from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder, \
    check_phone_number

# to get fields of User model
# User._meta.fields:


# the following function prepares the data to be used in the process of creating Excel file
def prepare_selected_query(selected_pages, paginator_obj, headers=None):
    full_name = []
    username = []
    organization = []
    job_type = []
    phone_number = []
    last_login = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Full Name":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        print("adding full name data")
                        full_name.append(user.full_name)
            elif header == "Username":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        username.append(user.username)
            elif header == "Organization":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        organization.append(user.organization)
            elif header == "JobType":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        job_type.append(user.job_type.name)
            elif header == "Phone Number":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        phone_number.append(user.phone_number)
            elif header == "Last Login":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    else:
        headers_here = ["Full Name", "Username", "Organization","JobType", "Phone Number", "Last Login"]
        print("headers are none")
        for page in range(1, paginator_obj.num_pages):
            for user in paginator_obj.page(page):
                full_name.append(user.full_name)
                username.append(user.username)
                organization.append(user.organization)
                job_type.append(user.job_type)
                phone_number.append("0" + user.phone_number)
                last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    return headers_here, full_name, username, organization,job_type, phone_number, last_login


def prepare_query(paginator_obj, headers=None):
    full_name = []
    username = []
    organization = []
    job_type = []
    phone_number = []
    last_login = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Full Name":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        full_name.append(user.full_name)
            elif header == "Username":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        username.append(user.username)
            elif header == "Organization":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        organization.append(user.organization)
            elif header == "JobType":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        job_type.append(user.job_type.name)
            elif header == "Phone Number":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        phone_number.append("0" + user.phone_number)
            elif header == "Last Login":
                for page in range(1, paginator_obj.num_pages + 1):
                    for user in paginator_obj.page(page):
                        last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    else:
        headers_here = ["Full Name", "Username", "Organization","JobType", "Phone Number", "Last Login"]
        for page in range(1, paginator_obj.num_pages + 1):
            for user in paginator_obj.page(page):
                full_name.append(user.full_name)
                username.append(user.username)
                organization.append(user.organization)
                if user.job_type:
                    job_type.append(user.job_type.name)
                phone_number.append("0" + user.phone_number)
                last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))

    # later for extracting actual data

    return headers_here, full_name, username, organization,job_type, phone_number, last_login


searchManObj = SearchMan("User")
report_man = ReportMan()

# new code starts here

class UsersListView(ListView):
    model = None
    template_name = None
    main_active_flag = None
    active_flag = None
    model_name = None
    no_records_admin = None
    no_records_monitor = None
    add_tool_tip_text = None
    update_tool_tip_text = None
    title = None
    searchManObj = SearchMan(model_name)
    # return default queryset used in this view
    def get_queryset(self):
        from apps.accounts.models import User
        return User.objects.all().order_by('-id')
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
        if  'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'full_name':
                print('here now in full name search')
                print(request.POST.get('clear'))
                search_message = request.POST.get('search_phrase')
                search_result = User.objects.filter(full_name=search_message).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Full Name')
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
                print('here now in organizaion')
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
                messages.error(request,
                               "Please choose an item from list , then write search phrase to search by it!")
                searchManObj.setSearchError(True)
            # if 'page' not in request.GET:
            #     instances = self.model.objects.all().order_by('-id')
            #     searchManObj.setPaginator(instances)
            #     searchManObj.setSearch(False)
        if  request.POST.get('clear') == 'clear':
            print("clear search")
            all_users = User.objects.all().order_by("id")
            searchManObj.setPaginator(all_users)
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
                "no_records_admin": self.no_records_admin,
                "no_records_monitor": self.no_records_monitor,
                "add_tool_tip_text": self.add_tool_tip_text,
                "update_tool_tip_text": self.update_tool_tip_text,
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
            "no_records_admin": self.no_records_admin,
            "no_records_monitor": self.no_records_monitor,
            "add_tool_tip_text": self.add_tool_tip_text,
            "update_tool_tip_text": self.update_tool_tip_text,
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

# new code ends here
@staff_member_required(login_url='login')
def all_users(request):
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
    from apps.accounts.models import User
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 5)

    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    # create search functionality
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'full_name':
            print('here now')
            search_message = request.POST.get('search_phrase')
            search_result = User.objects.filter(full_name=search_message).order_by("id")
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Full Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'username':
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
            search_phrase = request.POST.get('search_phrase')
            is_number_ok, phone_number = check_phone_number(search_phrase)
            if (is_number_ok):
                search_result = User.objects.filter(phone_number=phone_number).order_by("id")
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_phrase)
                searchManObj.setSearchOption('Phone Number')
                searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_users = User.objects.all().order_by("id")
        searchManObj.setPaginator(all_users)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_users = User.objects.all().order_by("id")
        searchManObj.setPaginator(all_users)
        searchManObj.setSearch(False)
    # create report functionality
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Full Name") if request.POST.get('full_name_header') is not None else ''
        headers.append("Username") if request.POST.get('username_header') is not None else ''
        headers.append("Organization") if request.POST.get('organization_header') is not None else ''
        headers.append("JobType") if request.POST.get('job_type_header') is not None else ''
        headers.append("Phone Number") if request.POST.get('phone_number_header') is not None else ''
        headers.append("Last Login") if request.POST.get('last_login_header') is not None else ''
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            # create a function that extracts only numbers from the string of selected pages numbers
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            # ends here
            if len(headers) > 0:
                constructor = {}
                headers, full_name, username, organization,job_type, phone_number, last_login = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(full_name) > 0:
                    constructor.update({"full_name": full_name})
                if len(username) > 0:
                    constructor.update({"username": username})
                if len(organization) > 0:
                    constructor.update({"organization": organization})
                if len(job_type) > 0:
                    constructor.update({"job_type": job_type})
                if len(phone_number) > 0:
                    constructor.update({"phone_number": phone_number})
                if len(last_login) > 0:
                    constructor.update({"last_login": last_login})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                  **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            else:
                headers = ["Full Name", "Username", "Organization","JobType", "Phone Number", "Last Login"]
                headers, full_name, username, organization,job_type, phone_number, last_login = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                  full_name=full_name,
                                                                                  username=username,
                                                                                  organization=organization,
                                                                                  job_type = job_type,
                                                                                  phone_number=phone_number,
                                                                                  last_login=last_login)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
        else:
            # get the original query of page and then structure the data
            query = searchManObj.getPaginator()
            print("empty query is ",query)
            print("headers are: ", headers)

            if len(headers) > 0:
                constructor = {}
                headers, full_name, username, organization,job_type, phone_number, last_login = prepare_query(query,
                                                                                                     headers=headers)
                if len(full_name) > 0:
                    print("full names are: ", full_name)
                    constructor.update({"full_name": full_name})
                if len(username) > 0:
                    constructor.update({"username": username})
                if len(organization) > 0:
                    constructor.update({"organization": organization})
                if len(job_type) > 0:
                    constructor.update({"job_type": job_type})
                if len(phone_number) > 0:
                    constructor.update({"phone_number": phone_number})
                if len(last_login) > 0:
                    constructor.update({"last_login": last_login})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                  **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    # request.session['temp_dir'] =  report_man.tempDir
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers, full_name, username, organization,job_type, phone_number, last_login = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Users', headers,
                                                                                  full_name=full_name,
                                                                                  username=username,
                                                                                  organization=organization,
                                                                                  job_type = job_type,
                                                                                  phone_number=phone_number,
                                                                                  last_login=last_login)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    # return redirect('download_file',filepath=filepath,filename=filename)

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
        users = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        users = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        users = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'accounts/all_users.html',
                  {
                      'title': _('All Users'),
                      'all_users': 'active',
                      'users':'active',
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
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
                  )






@staff_member_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
