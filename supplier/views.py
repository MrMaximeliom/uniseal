from rest_framework import viewsets
from Util.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages



# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify suppliers' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Other users can only use GET function on this endpoint
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "supplier_name",
     "image": "supplier_image_url",
     }
     Use other functions by accessing this url:
     supplier/<supplier's_id>
     Format of data will be as the previous data format for GET function
     To Search for particular supplier by its name use this url:
     supplier/?name=<supplier_name>
    """

    def get_view_name(self):
        return _("Create/Modify Suppliers' Data")


    from .serializers import SupplierSerializer
    serializer_class = SupplierSerializer

    def get_queryset(self):
        from .models import Supplier
        queryset = Supplier.objects.all().order_by("id")
        return queryset
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


# Dashboard Views
from django.contrib.auth.decorators import login_required
from .models import Supplier
suppliers = Supplier.objects.all().order_by("id")
@login_required(login_url='login')
def all_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/all_suppliers.html',
                  {
                      'title': _('All Suppliers'),
                      'all_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/edit_suppliers.html',
                  {
                      'title': _('Edit Suppliers'),
                      'edit_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def add_suppliers(request):
    from .forms import SupplierForm
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            supplier_name = form.cleaned_data.get('name')
            messages.success(request, f"New Supplier Added: {supplier_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SupplierForm()


    context = {
        'title': _('Add Suppliers'),
        'add_suppliers': 'active',
        'form': form,
    }
    return render(request, 'supplier/add_suppliers.html', context)
@login_required(login_url='login')
def delete_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/delete_suppliers.html',
                  {
                      'title': _('Delete Suppliers'),
                      'delete_suppliers': 'active',
                      'all_suppliers_data': supplier_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def edit_supplier(request,slug):
    from supplier.models import Supplier
    from .forms import SupplierForm
    obj = get_object_or_404(Supplier, slug=slug)
    print(obj.name)
    # if request.FILES['image']:

    supplier_form = SupplierForm(request.POST or None, instance=obj)
    if supplier_form.is_valid():
        if request.FILES:
            supplier = supplier_form.save()
            supplier.image = request.FILES['image']
            supplier.save()
        supplier_form.save()
        name = supplier_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {name} Data")
    else:
        for field, items in supplier_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))
    context = {
        'title': _('Edit Suppliers'),
        'edit_suppliers': 'active',
        'all_suppliers': suppliers,
        'form':supplier_form,
        'supplier':obj
    }
    return render(request, 'supplier/edit_supplier.html', context)

def confirm_delete(request,id):
    from supplier.models import Supplier
    obj = get_object_or_404(Supplier, id=id)
    try:
        obj.delete()
        messages.success(request, f"Supplier {obj.name} deleted successfully")
    except:
        messages.error(request, f"Supplier {obj.name} was not deleted , please try again!")


    return redirect('deleteSuppliers')