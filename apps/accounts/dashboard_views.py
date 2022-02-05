from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import rand_slug, SearchMan, createExelFile, ReportMan, delete_temp_folder, \
    check_phone_number


# the following function prepares the data to be used in the process of creating excel file
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
                job_type.append(user.job_type.name)
                phone_number.append("0" + user.phone_number)
                last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))

    # later for extracting actual data

    return headers_here, full_name, username, organization,job_type, phone_number, last_login


searchManObj = SearchMan("User")
report_man = ReportMan()

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
        set_default_headers = True
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
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                constructor = {}
                headers, full_name, username, organization,job_type, phone_number, last_login = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)

                if len(full_name) > 0:
                    print("full name is ", full_name)
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
def add_users(request):
    from .forms import UserRegistrationForm
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.slug = slugify(rand_slug())
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New User Added: {username}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = UserRegistrationForm()

    context = {
        'title': _('Add Users'),
        'add_users': 'active',
        'form': form,
        'users': 'active',

    }
    return render(request, 'accounts/add_users.html', context)


@staff_member_required(login_url='login')
def edit_user(request, slug):
    from apps.accounts.models import User
    from .forms import UserForm
    obj = get_object_or_404(User, slug=slug)
    user_form = UserForm(request.POST or None, instance=obj)
    if user_form.is_valid():
        user_form.save()
        username = user_form.cleaned_data.get('username')
        messages.success(request, f"Successfully Updated : {username} Data")
    else:
        for field, items in user_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit User'),
        'edit_user': 'active',
        'all_users': all_users,
        'user': obj,
        'form': user_form,
        'users': 'active',
    }
    return render(request, 'accounts/edit_user.html', context)


@staff_member_required(login_url='login')
def edit_users(request):
    from apps.accounts.models import User
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        USERNAME_SYNTAX_ERROR,
        FULL_NAME_SYNTAX_ERROR,
        ORGANIZATION_NAME_SYNTAX_ERROR,
        PHONE_NUMBER_SYNTAX_ERROR,
    CLEAR_SEARCH_TIP,
    SEARCH_USERS_TIP,
    )
    all_users = User.objects.all().order_by("id")
    search_result = ''
    paginator = Paginator(all_users, 5)
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

    return render(request, 'accounts/edit_users.html',
                  {
                      'title': _('Edit Users'),
                      'edit_users': 'active',
                      'users': 'active',
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
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
def delete_users(request):
    from apps.accounts.models import User
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 5)
    from apps.accounts.models import User
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        USERNAME_SYNTAX_ERROR,
        FULL_NAME_SYNTAX_ERROR,
        ORGANIZATION_NAME_SYNTAX_ERROR,
        PHONE_NUMBER_SYNTAX_ERROR,
        CLEAR_SEARCH_TIP,
        SEARCH_USERS_TIP,
    )
    all_users = User.objects.all().order_by("id")
    search_result = ''
    paginator = Paginator(all_users, 5)
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

    return render(request, 'accounts/delete_users.html',
                  {
                      'title': _('Delete Users'),
                      'delete_users': 'active',
                      'all_users': all_users,
                      'users': 'active',
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'current_user': request.user.username,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
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


def confirm_delete(request, id, url):
    from apps.accounts.models import User
    obj = get_object_or_404(User, id=id)
    try:
        obj.delete()
        messages.success(request, f"User {obj.username} deleted successfully")
    except:
        messages.error(request, f"User {obj.username} was not deleted , please try again!")

    return redirect(url)


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
