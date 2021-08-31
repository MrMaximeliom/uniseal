from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from django.contrib.auth.decorators import login_required

from address.models import Area
areas = Area.objects.annotate(num=Count('city')).order_by('-num')

def prepare_selected_query_city(selected_pages, paginator_obj, headers=None):
    area_list = []
    state_list = []
    city_list = []
    headers_here = ["City","State","Number of Areas"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "City":
                for page in selected_pages:
                    for city in paginator_obj.page(page):
                        city_list.append(city.name)
            elif header == "State":
                for page in selected_pages:
                    for city in paginator_obj.page(page):
                        state_list.append(city.state.name)
            elif header == "Number of Areas":
                for page in selected_pages:
                    for city in paginator_obj.page(page):
                        area_list.append(city.num_areas)

    else:
        for page in range(1, paginator_obj.num_pages + 1):
            for city in paginator_obj.page(page):
                city_list.append(city.name)
                state_list.append(city.state.name)
                area_list.append(city.num_areas)
    return headers_here, state_list,city_list,area_list


def prepare_query_city(paginator_obj, headers=None):
    states = []
    areas = []
    cities = []
    headers_here = ["City","State","Number of Areas"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "State":
                for page in range(1, paginator_obj.num_pages + 1):
                    for city in paginator_obj.page(page):
                        states.append(city.state.name)
            elif header == "City":
                for page in range(1, paginator_obj.num_pages + 1):
                    for city in paginator_obj.page(page):
                        cities.append(city.name)
            elif header == "Number of Areas":
                for page in range(1, paginator_obj.num_pages + 1):
                    for city in paginator_obj.page(page):
                        areas.append(city.num_areas)
    else:
        for page in range(1, paginator_obj.num_pages + 1):
            for city in paginator_obj.page(page):
                cities.append(city.name)
                states.append(city.state.name)
                areas.append(city.num_areas)
    return headers_here, states,cities,areas
search_man_cities = SearchMan("City")
report_man_cities = ReportMan()
@login_required(login_url='login')
def all_areas(request):
    paginator = Paginator(areas, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/all_areas.html',
                  {
                      'title': _('All Areas'),
                      'all_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@login_required(login_url='login')
def add_areas(request):
    from .forms import AreaForm
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            area = form.save()
            area.slug = slugify(rand_slug())
            area.save()
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Area Added: {name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = AreaForm()
    context = {
        'title': _('Add Areas'),
        'add_areas': 'active',
        'form': form
    }

    return render(request, 'address/add_areas.html', context)


@login_required(login_url='login')
def delete_areas(request):
    paginator = Paginator(areas, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/delete_areas.html',
                  {
                      'title': _('Delete Areas'),
                      'delete_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


@login_required(login_url='login')
def edit_areas(request):
    paginator = Paginator(areas, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        areas_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        areas_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        areas_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/edit_areas.html',
                  {
                      'title': _('Edit Areas'),
                      'edit_areas': 'active',
                      'all_areas_data': areas_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )


def edit_area(request, slug):
    from .models import Area
    from .forms import AreaForm
    # fetch the object related to passed id
    obj = get_object_or_404(Area, slug=slug)

    # pass the object as instance in form
    area_form = AreaForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if area_form.is_valid():
        area_form.save()
        name = area_form.cleaned_data.get('name')
        messages.success(request, f"Area {name} Updated")
    else:
        for field, items in area_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Area'),
        'edit_areas': 'active',
        'form': area_form,
        'area': obj,
    }
    return render(request, 'address/edit_area.html', context)


def confirm_area_delete(request, id):
    from .models import Area
    obj = get_object_or_404(Area, id=id)
    try:
        obj.delete()
        messages.success(request, f"Area {obj.name} deleted successfully")
    except:
        messages.error(request, f"Area {obj.name} was not deleted , please try again!")

    return redirect('deleteAreas')
