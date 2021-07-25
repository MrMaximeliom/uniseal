from rest_framework import viewsets
from Util.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
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
from .models import Supplier
suppliers = Supplier.objects.all().order_by("id")
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



def add_suppliers(request):
    from .forms import SupplierForm
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            supplier_name = form.cleaned_data.get('name')
            messages.success(request, f"New Supplier Added: {supplier_name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = SupplierForm()


    context = {
        'title': _('Add Suppliers'),
        'add_suppliers': 'active',
        'form': form,
    }
    return render(request, 'supplier/add_supplier.html', context)

def delete_suppliers(request):

    context = {
        'title': _('Delete Suppliers'),
        'delete_suppliers': 'active',
        'all_suppliers': suppliers,
    }
    return render(request, 'supplier/delete_suppliers.html', context)

def edit_suppliers(request):
    context = {
        'title': _('Edit Suppliers'),
        'edit_suppliers': 'active',
        'all_suppliers': suppliers,
    }
    return render(request, 'supplier/edit_suppliers.html', context)

