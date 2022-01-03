from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import views as auth_views
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@staff_member_required(login_url='login')
def dashboard(request):
    from accounts.models import User
    from product.models import Product
    from project.models import Project
    from brochures.models import Brochures
    users_count = User.objects.filter(admin=False).count()
    products_count = Product.objects.all().count()
    all_projects = Project.objects.all().order_by('-id')
    projects_count = all_projects.count()
    short_list_of_projects = all_projects[:5]
    brochures_count = Brochures.objects.all().count()
    context = {
        'title': _('Uniseal API Admin Dashboard'),
        'dashboard': 'active',
        'users_count': users_count,
        'products_count': products_count,
        'projects_count': projects_count,
        'brochures_count': brochures_count,
        'all_projects': short_list_of_projects,

    }
    return render(request, 'dashboard/index.html', context)


def products_categories_chart(request):
    from django.db.models import Count
    from category.models import Category
    labels = []
    data = []

    # queryset = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by(
    #     '-country_population')
    queryset = Category.objects.values('name').annotate(products_count=Count('product')).order_by("-products_count")

    for entry in queryset:
        labels.append(entry['name'])
        data.append(entry['products_count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
def users_registration_count_each_month_chart(request):
    from django.db.models import Count
    from accounts.models import User
    labels = []
    data = []

    # queryset = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by(
    #     '-country_population')
    queryset = User.objects.annotate(month=TruncMonth('registration_datetime')).values('month').annotate(total=Count('id')).order_by('-total')

    for entry in queryset:
        labels.append(entry['month'])
        data.append(entry['total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

class LoginView(auth_views.LoginView):
    template_name = 'dashboard/login.html'
    from accounts.forms import UserLoginForm
    from Util.utils import delete_temp_folder
    from Util.handle_login_form_strings import USERNAME_EMPTY_ERROR,USERNAME_BAD_FORMAT,PASSWORD_EMPTY_ERROR
    form_class = UserLoginForm
    delete_temp_folder()


    def form_valid(self, form):
        from django.contrib.auth import login as auth_login
        from django.http import HttpResponseRedirect
        """Security check complete. Log the user in."""
        current_user = form.get_user()
        phone_number = current_user.phone_number
        print("user entered phone number is: ",phone_number)
        if phone_number.startswith("0"):
            if phone_number.startswith("0"):
                phone_without_zero = phone_number[1:]
                print("phone without 0 is: ",phone_without_zero)
        if current_user.staff:
            auth_login(self.request, form.get_user())
            username = current_user.username
            messages.success(self.request,f" Welcome {username} Have a nice day")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request,_('Phone Number or Password Error for Staff User'))

        return redirect('login')

    extra_context = {
        'title':_('Login Page'),
        'invalid_login':_('Phone Number or Password Error for Staff User'),
        'hide_footer':True,
        'data_js': {
            "username_empty_error": USERNAME_EMPTY_ERROR,
            "username_bad_format": USERNAME_BAD_FORMAT,
            "password_empty_error": PASSWORD_EMPTY_ERROR,
        }


    }


def ForgotPassword(request):
    pass
def Login(request):
    from accounts.forms import UserLoginForm

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['phone_number']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.staff:
                    login(request, user)
                else:
                    messages.error(request, _("Username or Password error for staff user"))
                # Redirect to a success page.

            else:
                messages.error(request, _("Username or Password error for staff user"))
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = UserLoginForm()
    context = {
        'title': _('Add Users'),
        'add_users': 'active',
        'form': form,

    }

    return render(request,"dashboard/login.html",context)



def logout_view(request):
    user = request.user.username
    logout(request)
    messages.success(request, f" Good Bye {user} Come Back Again")
    return redirect('login')
