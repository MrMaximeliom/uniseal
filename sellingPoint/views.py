from django.template.defaultfilters import slugify

from Util.permissions import UnisealPermission
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from Util.utils import rand_slug


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
    def get_queryset(self):
        from .models import SellingPoint
        queryset = SellingPoint.objects.all().order_by('id')
        return queryset


    from .serializers import SellingPointSerializer
    serializer_class = SellingPointSerializer

    permission_classes = [UnisealPermission]




#

# Views for dashboard
from sellingPoint.models import SellingPoint
sellingPoints = SellingPoint.objects.all().order_by("id")
@login_required(login_url='login')
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
@login_required(login_url='login')
def add_selling_points(request):
    from .forms import SellingPointForm
    if request.method == 'POST':
        form = SellingPointForm(request.POST,request.FILES)
        if form.is_valid():
            # point = form.save()
            # point.slug = slugify(rand_slug())
            # point.save()
            form.save()
            point_name = form.cleaned_data.get('name')
            messages.success(request, f"Successfully Added Selling Point : {point_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = SellingPointForm()

    context = {
        'title': _('Add Selling Points'),
        'add_selling_points': 'active',
        'form': form,
    }
    return render(request, 'sellingPoints/add_selling_points.html', context)
@login_required(login_url='login')
def delete_selling_points(request):
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

    return render(request, 'sellingPoints/delete_selling_points.html',
                  {
                      'title': _('Delete Selling Points'),
                      'all_selling_points': 'active',
                      'all_selling_points_data': selling_points,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
@login_required(login_url='login')
def edit_selling_points(request):
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

    return render(request, 'sellingPoints/edit_selling_points.html',
                  {
                      'title': _('Edit Selling Points'),
                      'all_selling_points': 'active',
                      'all_selling_points_data': selling_points,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def edit_selling_point(request,slug):
    from .models import SellingPoint
    from .forms import SellingPointForm
    obj = get_object_or_404(SellingPoint, slug=slug)

    # pass the object as instance in form
    point_form = SellingPointForm(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if point_form.is_valid()  :
        if request.FILES:
            project = point_form.save()
            project.image = request.FILES['image']
            project.save()
        point_form.save()
        point_name = point_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {point_name} Data")
    else:
        for field, items in point_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Selling Points'),
        'edit_selling_points': 'active',
        'form':point_form,
        'selling_point' : obj,

    }
    return render(request, 'sellingPoints/edit_selling_point.html', context)

@login_required(login_url='login')
def selling_point_details(request,slug):
    from .models import SellingPoint
    point = get_object_or_404(SellingPoint, slug=slug)


    return render(request, 'sellingPoints/selling_point_detail.html',
                  {
                      'title': _('Selling Point Details'),
                      'all_products': 'active',
                      'point_data': point,
                  }
                  )
def confirm_delete(request,id):
    from .models import SellingPoint
    obj = get_object_or_404(SellingPoint, id=id)
    try:
        obj.delete()
        messages.success(request, f"Selling Point: {obj.name} deleted successfully")
    except:
        messages.error(request, f"Selling Point: {obj.name} was not deleted , please try again!")


    return redirect('deleteSellingPoints')