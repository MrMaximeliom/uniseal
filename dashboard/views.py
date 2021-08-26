from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy  as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout, login
# Create your views here.
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
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
    extra_context = {
        'title':_('Login Page'),


    }


def testing_view(request):
    return render(request,'dashboard/testing.html')





def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page