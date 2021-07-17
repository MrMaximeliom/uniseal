from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.utils.translation import gettext_lazy as _

class  CityViewSet(viewsets.ModelViewSet):
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
        "country": country_id,
       }
      Use PUT function by accessing this url:
      /city/<city's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CitySerializer

    def get_view_name(self):
        return _("Create/Modify Cities' Data")

    from address.models import City
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [UnisealPermission]

class  CountryViewSet(viewsets.ModelViewSet):
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
      /country/<country's_id>
      Format of data will be as the previous data format for GET function

      """
    from address.serializers import CountrySerializer

    def get_view_name(self):
        return _("Create/Modify Countries' Data")

    from address.models import Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [UnisealPermission]

#Views for dashboard - cities views
from address.models import City
# cities = City.objects.all()
cities = City.objects.annotate(num_users=Count('user')).order_by('-num_users')

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

def add_cities(request):

    context = {
        'title': _('Add Cities'),
        'add_cities': 'active',
        'all_cities': cities,
    }
    return render(request, 'address/add_cities.html', context)

def delete_cities(request):

    context = {
        'title': _('Delete Cities'),
        'delete_cities': 'active',
        'all_categories': cities,
    }
    return render(request, 'address/delete_cities.html', context)

def edit_cities(request):
    context = {
        'title': _('Edit Cities'),
        'edit_cities': 'active',
        'all_categories': cities,
    }
    return render(request, 'address/edit_cities.html', context)


from address.models import Country
# countries = Country.objects.all()
countries = Country.objects.annotate(num_users=Count('city')).order_by('-num_users')
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

def add_countries(request):

    context = {
        'title': _('Add Countries'),
        'add_countries': 'active',
        'all_countries': countries,
    }
    return render(request, 'address/add_countries.html', context)

def delete_countries(request):

    context = {
        'title': _('Delete Countries'),
        'delete_countries': 'active',
        'all_countries': countries,
    }
    return render(request, 'address/delete_countries.html', context)

def edit_countries(request):
    context = {
        'title': _('Edit Countries'),
        'edit_countries': 'active',
        'all_countries': countries,
    }
    return render(request, 'address/edit_countries.html', context)
