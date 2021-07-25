from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


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
            form.save()
            country_name = form.cleaned_data.get('name')
            messages.success(request, f"New Country Added: {country_name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
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
    context = {
        'title': _('Delete Countries'),
        'delete_countries': 'active',
        'all_countries': countries,
    }
    return render(request, 'address/delete_countries.html', context)

@login_required(login_url='login')
def edit_countries(request):
    context = {
        'title': _('Edit Countries'),
        'edit_countries': 'active',
        'all_countries': countries,
    }
    return render(request, 'address/edit_countries.html', context)


from address.models import City

# cities = City.objects.all()
cities = City.objects.annotate(num_users=Count('user')).order_by('-num_users')

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
            form.save()
            city = form.cleaned_data.get('name')
            messages.success(request, f"New City Added: {city}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
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
    context = {
        'title': _('Delete Cities'),
        'delete_cities': 'active',
        'all_categories': cities,
    }
    return render(request, 'address/delete_cities.html', context)

@login_required(login_url='login')
def edit_cities(request):
    context = {
        'title': _('Edit Cities'),
        'edit_cities': 'active',
        'all_categories': cities,
    }
    return render(request, 'address/edit_cities.html', context)


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
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New State Added: {name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
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
    context = {
        'title': _('Delete States'),
        'delete_states': 'active',
        'all_states': states,
    }
    return render(request, 'address/delete_states.html', context)

@login_required(login_url='login')
def edit_states(request):
    context = {
        'title': _('Edit States'),
        'edit_states': 'active',
        'all_states': states,
    }
    return render(request, 'address/edit_states.html', context)


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
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"New Area Added: {name}")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
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
    context = {
        'title': _('Delete Areas'),
        'delete_areas': 'active',
        'all_areas': areas,
    }
    return render(request, 'address/delete_areas.html', context)

@login_required(login_url='login')
def edit_areas(request):
    context = {
        'title': _('Edit Areas'),
        'edit_areas': 'active',
        'all_areas': areas,
    }
    return render(request, 'address/edit_areas.html', context)
