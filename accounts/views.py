from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework import mixins
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from Util.utils import EnablePartialUpdateMixin, rand_slug , SearchMan,createExelFile
from Util.permissions import IsSystemBackEndUser, IsAnonymousUser, UnisealPermission
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages



# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect

class Logout(APIView):
    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework.response import Response
        from rest_framework import status
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModifyUserDataViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
          API endpoint that allows to modify users' data by Admin Only
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
          Data will be retrieved in the following format using GET function:
        {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
         "email": "ali@gmail.com",
         "gender": "male",
         "phone_number": "0922367654",
         "city": "city_id",


    }
    Use PUT function by accessing this url:
    /accounts/modifyUsersData/<user's_id>
    Format of data will be as the previous data format for GET function

        """
    from accounts.serializers import RegisterSerializer
    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsSystemBackEndUser]

    def get_view_name(self):
        return _("Modify Users' Data")


class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        API endpoint that allows to register new users
        this endpoint allows only POST function
        permissions to this view is restricted as the following:
        - anonymous users and system backend users (Admin and Staff )
         only can access this api to create an account
         Data will be submitted in the following format using POST function:
       {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
        "password":"password",
        "confirm_password":"confirm_password",
        "email": "ali@gmail.com",
        "gender": "male",
        "phone_number": "922367654",
        "city":"city_id",

        }
      """
    from accounts.serializers import RegisterSerializer

    def get_view_name(self):
        return _("Register New User")

    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser]


class ChangePasswordView(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
        An endpoint for changing password.
        """
    from accounts.serializers import ChangePasswordSerializer

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from .models import User
        return User.objects.filter(id=self.request.user.id)


class CurrentUserDataViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet
                             ):
    """
      API endpoint that allows to view current user data
      this endpoint allows GET,PUT,PATCH functions
      permissions to this view is restricted as the following:
      - any user role (admin - staff - customer - seller - logistic)
       currently logged into the system can use this view to get his/her data
      Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
        "email": "ali@gmail.com",
        "gender": "male",
        "phone_number": "922367654",
        "password":"encrypted_password"
        "city":"city_id",

        }
    Use PUT function by accessing this url:
    /accounts/me/<user's_id>
    Format of data will be as the previous data format for GET function
    """
    from accounts.serializers import UserSerializer
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from .models import User
        return User.objects.filter(id=self.request.user.id)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #
    #     return self.update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     from accounts.serializers import UserSerializer
    #     serialized = UserSerializer(request.user, data=request.data, partial=True)
    #     return self.update(request, *args, **kwargs)
    # def patch(self, request, pk):
    #     from accounts.serializers import UserSerializer
    #     object = self.get_object(pk)
    #     serializer = UserSerializer(object, data=request.data,
    #                                      partial=True)  # set partial=True to update a data partially
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(code=201, data=serializer.data)

    def get_view_name(self):
        return _("Current User's Data")


class ContactUsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify messages by
        registered users
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions  this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "phone_number": phone_number,
        "email": "email",
        "name": "name",
        "address": "address",
        "message": "message",
        "website": "website_url",
        "facebook": "facebook_url",
        "twitter": "twitter_url",
        "linkedin": "linkedin_url",
        "instagram": "instagram_url",
    }
    Use PUT function by accessing this url:
    /contactUs/<contactUsMessages's_id>
    Format of data will be as the previous data format for GET function

      """
    from accounts.serializers import ContactUsSerializer

    def get_view_name(self):
        return _("Create/Modify Contact Us Message")

    from accounts.models import ContactUs
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [UnisealPermission]



# Views for dashboard
from django.contrib.auth.decorators import login_required
# the following function prepares the data to be used in the process of creating excel file
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    full_name = []
    username = []
    organization = []
    phone_number = []
    last_login = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Full Name":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        full_name.append(user.full_name)
            elif header == "Username":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        username.append(user.username)
            elif header == "Organization":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        organization.append(user.organization)
            elif header == "Phone Number":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        phone_number.append(user.phone_number)
            elif header == "Last Login":
                for page in selected_pages:
                    for user in paginator_obj.page(page):
                        last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    else:
        headers_here = ["Full Name", "Username", "Organization", "Phone Number", "Last Login"]
        for page in range(1, paginator_obj.num_pages):
            for user in paginator_obj.page(page):
                full_name.append(user.full_name)
                username.append(user.username)
                organization.append(user.organization)
                phone_number.append("0" + user.phone_number)
                last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    return headers_here, full_name, username, organization, phone_number, last_login






def prepare_query(paginator_obj,headers=None):
    full_name = []
    username = []
    organization = []
    phone_number = []
    last_login = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Full Name":
                for page in range(1, paginator_obj.num_pages):
                    for user in paginator_obj.page(page):
                        full_name.append(user.full_name)
            elif header == "Username":
                for page in range(1, paginator_obj.num_pages):
                    for user in paginator_obj.page(page):
                        username.append(user.username)
            elif header == "Organization":
                for page in range(1, paginator_obj.num_pages):
                    for user in paginator_obj.page(page):
                        organization.append(user.organization)
            elif header == "Phone Number":
                for page in range(1, paginator_obj.num_pages):
                    for user in paginator_obj.page(page):
                        phone_number.append("0"+user.phone_number)
            elif header == "Last Login":
                for page in range(1, paginator_obj.num_pages):
                    for user in paginator_obj.page(page):
                        last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))
    else:
        headers_here = ["Full Name","Username","Organization","Phone Number","Last Login"]
        for page in range(1, paginator_obj.num_pages):
            for user in paginator_obj.page(page):
                full_name.append(user.full_name)
                username.append(user.username)
                organization.append(user.organization)
                phone_number.append("0"+user.phone_number)
                last_login.append(user.last_login.strftime('%d-%m-%y %a %H:%M %p'))

    # later for extracting actual data


    return headers_here,full_name,username,organization,phone_number,last_login

def download_file(request):
    import os,mimetypes
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'test.xlsx'
    # Define the full file path
    filepath = BASE_DIR  + "/"+filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
searchManObj = SearchMan("User")
@login_required(login_url='login')
def all_users(request):
    from accounts.models import User
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 5)

    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST :
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
            search_result = User.objects.filter(phone_number=search_phrase).order_by("id")
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
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Full Name") if request.POST.get('full_name_header') is not None else ''
        headers.append("Username") if request.POST.get('username_header') is not None else ''
        headers.append("Organization") if request.POST.get('organization_header') is not None else ''
        headers.append("Phone Number") if request.POST.get('phone_number_header') is not None else ''
        headers.append("Last Login") if request.POST.get('last_login_header') is not None else ''
        if request.POST.get('allData') == 'allData':
            # get the original query of page and then structure the data
            query = searchManObj.getPaginator()

            if len(headers) > 0 :
                constructor = {}
                headers, full_name, username, organization, phone_number, last_login = prepare_query(query,headers=headers)
                if len(full_name) > 0 :
                    constructor.update({"full_name": full_name})
                if len(username) > 0:
                    constructor.update({"username": username})
                if len(organization) > 0:
                    constructor.update({"organization": organization})
                if len(phone_number) > 0:
                    constructor.update({"phone_number": phone_number})
                if len(last_login) > 0:
                    constructor.update({"last_login": last_login})
                createExelFile('Report_For_Users',headers, **constructor)
                # if status:
                #     messages.success(request,f"Report Successfully Created ")
                # else:
                #     messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers, full_name, username, organization, phone_number, last_login = prepare_query(query)
                createExelFile('Report_For_Users',headers, full_name=full_name, username=username,
                               organization=organization, phone_number=phone_number, last_login=last_login)
                # if status:
                #     messages.success(request,f"Report Successfully Created")
                # else:
                #     messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


        elif request.POST.get('pages_collector') != 'none':
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ",request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                constructor = {}
                headers, full_name, username, organization, phone_number, last_login = prepare_selected_query(selected_pages=selected_pages,paginator_obj=query,
                                                                                                     headers=headers)
                if len(full_name) > 0:
                    constructor.update({"full_name": full_name})
                if len(username) > 0:
                    constructor.update({"username": username})
                if len(organization) > 0:
                    constructor.update({"organization": organization})
                if len(phone_number) > 0:
                    constructor.update({"phone_number": phone_number})
                if len(last_login) > 0:
                    constructor.update({"last_login": last_login})
                createExelFile('Report_For_Users',headers, **constructor)
                # if status:
                #     messages.success(request,f"Report Successfully Created ")
                # else:
                #     messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, full_name, username, organization, phone_number, last_login = prepare_selected_query(selected_pages,query,headers)
                createExelFile('Report_For_Users',headers, full_name=full_name, username=username,
                               organization=organization, phone_number=phone_number, last_login=last_login)
                # if status:
                #     messages.success(request,f"Report Successfully Created ")
                # else:
                #     messages.error(request, "Sorry Report Failed To Create , Please Try Again!")



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
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error':searchManObj.getSearchError()
                  }
                  )


@login_required(login_url='login')
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

    }
    return render(request, 'accounts/add_users.html', context)


@login_required(login_url='login')
def edit_user(request,slug):
    from accounts.models import User
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
        'user':obj,
        'form':user_form
    }
    return render(request, 'accounts/edit_user.html', context)

@login_required(login_url='login')
def edit_users(request):
    from accounts.models import User
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
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
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def delete_users(request):
    from accounts.models import User
    all_users = User.objects.all().order_by("id")
    paginator = Paginator(all_users, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
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
                      'all_users':all_users,
                      'all_users_data': users,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'current_user':request.user.username
                  }
                  )

def confirm_delete(request,id,url):
    from accounts.models import User
    obj = get_object_or_404(User, id=id)
    try:
        obj.delete()
        messages.success(request, f"User {obj.username} deleted successfully")
    except:
        messages.error(request, f"User {obj.username} was not deleted , please try again!")

    return redirect(url)
@login_required(login_url='login')
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