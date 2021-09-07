from django.shortcuts import render
from django.utils.translation import gettext_lazy  as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout, login,authenticate

# Create your views here.
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
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

class LoginView(auth_views.LoginView):
    template_name = 'dashboard/login.html'

    def form_valid(self, form):
        from django.contrib.auth import login as auth_login
        from django.http import HttpResponseRedirect
        """Security check complete. Log the user in."""
        current_user = form.get_user()
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


    }



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
    # from accounts.models import User
    # user = User.objects.get(u=request.user)
    # username = user.username
    messages.success(request, f" Good Bye {user} Come Back Again")
    return redirect('login')
    # Redirect to a success page