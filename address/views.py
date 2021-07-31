from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug


class CityViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify cities by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "city_name",
        "state": state_id,
       }
      Use PUT function by accessing this url:
      /address/modifyCity/<city's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CitySerializer

    def get_view_name(self):
        return _("Create/Modify Cities' Data")

    from address.models import City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [UnisealPermission]


class CountryViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify countries by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "country_name",

       }
      Use PUT function by accessing this url:
      /address/modifyCountry/<country's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CountrySerializer

    def get_view_name(self):
        return _("Create/Modify Countries' Data")

    from address.models import Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [UnisealPermission]


class StateViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify states by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "country_name",
        "country": country_id,

       }
      Use PUT function by accessing this url:
      /address/modifyState/<country's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import StateSerializer

    def get_view_name(self):
        return _("Create/Modify States' Data")

    from address.models import State
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [UnisealPermission]


class AreaViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify areas by
        the admin
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions to this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "name": "area_name",
        "city": city_id,

       }
      Use PUT function by accessing this url:
      /address/modifyArea/<area's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import AreaSerializer

    def get_view_name(self):
        return _("Create/Modify Areas' Data")

    from address.models import Area
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [UnisealPermission]


# Views for dashboard - cities views
from address.models import Country
from django.contrib.auth.decorators import login_required

# countries = Country.objects.all()
countries = Country.objects.annotate(num_users=Count('state')).order_by('-num_users')

@login_required(login_url='login')
def all_countries(request):
    paginator = Paginator(countries, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        countries_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        countries_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        countries_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/all_countries.html',
                  {
                      'title': _('All Countries'),
                      'all_countries': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def add_countries(request):
    from .forms import CountryForm
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            country.slug = slugify(rand_slug())
            country.save()
            country_name = form.cleaned_data.get('name')
            messages.success(request, f"New Country Added: {country_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = CountryForm()
    context = {
        'title': _('Add Countries'),
        'add_countries': 'active',
        'all_countries': countries,
        'form': form
    }

    return render(request, 'address/add_countries.html', context)

@login_required(login_url='login')
def delete_countries(request):
    paginator = Paginator(countries, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        countries_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        countries_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        countries_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/delete_countries.html',
                  {
                      'title': _('Delete Countries'),
                      'delete_countries': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def edit_countries(request):
    paginator = Paginator(countries, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        countries_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        countries_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        countries_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/edit_countries.html',
                  {
                      'title': _('Edit Countries'),
                      'edit_countries': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def edit_country(request,slug):
    from .models import Country
    from .forms import CountryForm
    # fetch the object related to passed id
    obj = get_object_or_404(Country, slug=slug)

    # pass the object as instance in form
    country_form = CountryForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if country_form.is_valid()  :
        country_form.save()
        name =  country_form.cleaned_data.get('name')
        messages.success(request, f"Country {name} Updated")
    else:
        for field, items in country_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Country'),
        'edit_countries': 'active',
        'form':country_form,
        'country' : obj,
    }
    return render(request,'address/edit_country.html',context)

def confirm_country_delete(request,id):
    from .models import Country
    obj = get_object_or_404(Country, id=id)
    try:
        obj.delete()
        messages.success(request, f"Country {obj.name} deleted successfully")
    except:
        messages.error(request, f"Country {obj.name} was not deleted , please try again!")


    return redirect('deleteCountries')

from address.models import City

cities = City.objects.all().order_by('id')
# cities = City.objects.annotate(num_users=Count('user')).order_by('-num_users')

@login_required(login_url='login')
def all_cities(request):
    paginator = Paginator(cities, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        cities_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        cities_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        cities_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/all_cities.html',
                  {
                      'title': _('All Cities'),
                      'all_cities': 'active',
                      'all_cities_data': cities_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def add_cities(request):
    from .forms import CityForm
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save()
            city.slug = slugify(rand_slug())
            city.save()
           
            city = form.cleaned_data.get('name')
            messages.success(request, f"New City Added: {city}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = CityForm()
    context = {
        'title': _('Add Cities'),
        'add_cities': 'active',
        'form': form
    }

    return render(request, 'address/add_cities.html', context)

@login_required(login_url='login')
def delete_cities(request):
    paginator = Paginator(cities, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        cities_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        cities_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        cities_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/delete_cities.html',
                  {
                      'title': _('Delete Cities'),
                      'delete_cities': 'active',
                      'all_cities_data': cities_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def edit_cities(request):
    paginator = Paginator(cities, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        cities_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        cities_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        cities_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/edit_cities.html',
                  {
                      'title': _('Edit Cities'),
                      'edit_cities': 'active',
                      'all_cities_data': cities_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def edit_city(request,slug):
    from .models import City
    from .forms import CityForm
    # fetch the object related to passed id
    obj = get_object_or_404(City, slug=slug)

    # pass the object as instance in form
    city_form = CityForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if city_form.is_valid()  :
        city_form.save()
        name =  city_form.cleaned_data.get('name')
        messages.success(request, f"City {name} Updated")
    else:
        for field, items in city_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit City'),
        'edit_countries': 'active',
        'form':city_form,
        'city' : obj,
    }
    return render(request,'address/edit_city.html',context)

def confirm_city_delete(request,id):
    from .models import City
    obj = get_object_or_404(City, id=id)
    try:
        obj.delete()
        messages.success(request, f"City {obj.name} deleted successfully")
    except:
        messages.error(request, f"City {obj.name} was not deleted , please try again!")


    return redirect('deleteCities')

# states goes here

from address.models import State

# cities = City.objects.all()
states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')

@login_required(login_url='login')
def all_states(request):
    paginator = Paginator(states, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        states_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        states_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        states_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/all_states.html',
                  {
                      'title': _('All States'),
                      'all_states': 'active',
                      'all_states_data': states_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def add_states(request):
    from .forms import StateForm
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            state = form.save()
            state.slug = slugify(rand_slug())
            state.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New State Added: {name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = StateForm()
    context = {
        'title': _('Add States'),
        'add_states': 'active',
        'form': form
    }

    return render(request, 'address/add_states.html', context)

@login_required(login_url='login')
def delete_states(request):
    paginator = Paginator(states, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        states_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        states_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        states_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/delete_states.html',
                  {
                      'title': _('Delete States'),
                      'delete_states': 'active',
                      'all_states_data': states_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )

@login_required(login_url='login')
def edit_states(request):
    paginator = Paginator(states, 5)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        states_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        states_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        states_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'address/edit_states.html',
                  {
                      'title': _('Edit States'),
                      'edit_states': 'active',
                      'all_states_data': states_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page
                  }
                  )
def edit_state(request,slug):
    from .models import State
    from .forms import StateForm
    # fetch the object related to passed id
    obj = get_object_or_404(State, slug=slug)

    # pass the object as instance in form
    state_form = StateForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if state_form.is_valid()  :
        state_form.save()
        name =  state_form.cleaned_data.get('name')
        messages.success(request, f"State {name} Updated")
    else:
        for field, items in state_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit State'),
        'edit_states': 'active',
        'form':state_form,
        'state' : obj,
    }
    return render(request,'address/edit_state.html',context)

def confirm_state_delete(request,id):
    from .models import State
    obj = get_object_or_404(State, id=id)
    try:
        obj.delete()
        messages.success(request, f"State {obj.name} deleted successfully")
    except:
        messages.error(request, f"State {obj.name} was not deleted , please try again!")


    return redirect('deleteStates')

# areas goes here

from address.models import Area

# cities = City.objects.all()
areas = Area.objects.annotate(num=Count('city')).order_by('-num')

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

def edit_area(request,slug):
    from .models import Area
    from .forms import AreaForm
    # fetch the object related to passed id
    obj = get_object_or_404(Area, slug=slug)

    # pass the object as instance in form
    area_form = AreaForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if area_form.is_valid()  :
        area_form.save()
        name =  area_form.cleaned_data.get('name')
        messages.success(request, f"Area {name} Updated")
    else:
        for field, items in area_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Area'),
        'edit_areas': 'active',
        'form':area_form,
        'area' : obj,
    }
    return render(request,'address/edit_area.html',context)

def confirm_area_delete(request,id):
    from .models import Area
    obj = get_object_or_404(Area, id=id)
    try:
        obj.delete()
        messages.success(request, f"Area {obj.name} deleted successfully")
    except:
        messages.error(request, f"Area {obj.name} was not deleted , please try again!")


    return redirect('deleteAreas')