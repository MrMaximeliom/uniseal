from django.shortcuts import render
from django.utils.translation import gettext as _
# Create your views here.
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
    context = {
        'title':  _('Uniseal API Admin Dashboard'),
        'dashboard' : 'active',
        'users_count':users_count,
        'products_count':products_count,
        'projects_count':projects_count,
        'brochures_count':brochures_count,
        'all_projects':short_list_of_projects,

    }
    return render(request, 'dashboard/index.html', context)
def products(request):
    context = {
        'title':_('Products'),
        'products':'active',
    }
    return render(request,'dashboard/products.html',context)