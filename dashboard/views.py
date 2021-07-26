from django.shortcuts import render
from django.utils.translation import gettext_lazy  as _
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
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
    all_projects = Project.objects.all()
    projects_count = all_projects.count()
    short_list_of_projects = all_projects[:5]
    brochures_count = Brochures.objects.all().count()

    all_fields =User._meta.fields
    print(all_fields)
    print(request.user)
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
        'title':_('Login Page')
    }

    # def get_success_url(self):
    #     return resolve_url('dashboard:dashboard')

# def login_user(request):
#     from django.contrib.auth import authenticate
#     from accounts.forms import UserLoginForm
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             print('user authenticated')
#             login(request,user)
#             # return redirect('dashboard')
#
#         else:
#             print('user is not authenticated')
#             return redirect('login')
#             # for msg in form.error_messages:
#             #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
#     else:
#         form = UserLoginForm()
#     # if request.method == "GET":
#     #     pass
#     #
#     # else:
#     #
#     #     email = request.POST['email']
#     #     password = request.POST['password']
#     #     user = authenticate(request, username=email, password=password)
#     #     if user is not None:
#     #         login(request)
#     #         return redirect('dashboard')
#     #
#     #     else:
#     #         return redirect('login')
#
#     return render(request, 'dashboard/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page