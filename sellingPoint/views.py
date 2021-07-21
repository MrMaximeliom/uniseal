from Util.permissions import UnisealPermission
from rest_framework import viewsets
from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class SellingPointViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify selling points' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":12,
     "name": "selling_point_name",
     "image":"selling_point_image_url",
     "location":"selling_point_location",
     "address":"selling_point_address",
     "city":"city_id",
     "area":"area_id",
     "phone_number":"phone_number",
     "secondary_phone":"secondary_phone_number",
     "email":"email",
     }
     Use other functions by accessing this url:
     sellingPoint/createSellingPoint/<sellingPoint's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Create/Modify Selling Points")

    from .serializers import SellingPointSerializer
    serializer_class = SellingPointSerializer
    from .models import SellingPoint
    permission_classes = [UnisealPermission]
    queryset = SellingPoint.objects.all()




#

# Views for dashboard
from sellingPoint.models import SellingPoint
sellingPoints = SellingPoint.objects.all().order_by("id")
def all_selling_points(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(sellingPoints, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        selling_points = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        selling_points = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        selling_points = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'sellingPoints/all_selling_points.html',
                  {
                      'title': _('All Selling Points'),
                      'all_selling_points': 'active',
                      'all_selling_points_data': selling_points,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

def add_selling_points(request):
    from .forms import SellingPointForm
    if request.method == 'POST':
        form = SellingPointForm(request.POST)
        if form.is_valid():
            form.save()
            selling_point_name = form.cleaned_data.get('name')
            messages.success(request, f"New User Added: {selling_point_name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = SellingPointForm()

    context = {
        'title': _('Add Selling Points'),
        'add_selling_points': 'active',
        'form': form,
    }
    return render(request, 'sellingPoints/add_selling_points.html', context)

def delete_selling_points(request):

    context = {
        'title': _('Delete Selling Points'),
        'delete_selling_points': 'active',
        'all_selling_points': sellingPoints,
    }
    return render(request, 'sellingPoints/delete_selling_points.html', context)

def edit_selling_points(request):
    context = {
        'title': _('Edit Selling Points'),
        'edit_selling_points': 'active',
        'all_selling_points': sellingPoints,
    }
    return render(request, 'sellingPoints/edit_selling_points.html', context)

