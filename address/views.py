from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from rest_framework import viewsets
from Util.permissions import UnisealPermission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from Util.utils import rand_slug
from Util.utils import  SearchMan,createExelFile,ReportMan,delete_temp_folder


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
countries = Country.objects.all().order_by('id')
def prepare_selected_query_country(selected_pages,paginator_obj,headers=None):
    country_list = []
    headers_here = ["Country"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Country":
                for page in selected_pages:
                    for country in paginator_obj.page(page):
                        country_list.append(country.name)
    else:
        for page in range(1, paginator_obj.num_pages+1):
            for country in paginator_obj.page(page):
                country_list.append(country.name)
    return headers_here, country_list
def prepare_query_country(paginator_obj,headers=None):
    countries = []
    headers_here = ["Country"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Country":
                for page in range(1, paginator_obj.num_pages+1):
                    for category in paginator_obj.page(page):
                        countries.append(category.name)
    else:
        for page in range(1, paginator_obj.num_pages+1):
            for category in paginator_obj.page(page):
                countries.append(category.name)
    return headers_here, countries
@login_required(login_url='login')
def all_countries(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''
    searchManObj = SearchMan("Country")
    report_man = ReportMan()
    paginator = Paginator(countries, 5)
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Country')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, countries_list  = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = searchManObj.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers,category=countries_list,
                                                                                 )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = searchManObj.getPaginator()
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
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
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
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''
    searchManObj = SearchMan("Country")
    report_man = ReportMan()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Country')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, countries_list  = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = searchManObj.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers,category=countries_list,
                                                                                 )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = searchManObj.getPaginator()
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
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
                  }
                  )

@login_required(login_url='login')
def edit_countries(request):
    paginator = Paginator(countries, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''
    searchManObj = SearchMan("Country")
    report_man = ReportMan()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Country')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        searchManObj.setPaginator(all_countries)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, countries_list  = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = searchManObj.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Countries',
                                                                                  headers,category=countries_list,
                                                                                 )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter

        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = searchManObj.getPaginator()
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
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
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
def prepare_selected_query_state(selected_pages,paginator_obj,headers=None):
    states_list = []
    cities_list = []
    countries_list = []
    headers_here = ["State","Country", "Number of Cities"]
    if headers is not None:
        print("in selected query headers are not none")
        headers_here = headers
        for header in headers_here:
            if header == "State":
                for page in selected_pages:
                    for state in paginator_obj.page(page):
                        states_list.append(state.name)
            elif header == "Country":
                for page in selected_pages:
                    for state in paginator_obj.page(page):
                        countries_list.append(state.country.name)
            elif header == "Number of Cities":
                for page in selected_pages:
                    for state in paginator_obj.page(page):
                        cities_list.append(state.num_cities)
    else:
        for page in range(1, paginator_obj.num_pages+1):
            for state in paginator_obj.page(page):
                cities_list.append(state.num_cities)
                states_list.append(state.name)
                countries_list.append(state.country.name)
    return headers_here, states_list,countries_list,cities_list
def prepare_query_state(paginator_obj,headers=None):
    states_list = []
    cities_list = []
    countries_list = []
    headers_here = ["State","Country","Number of Cities"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "State":
                for page in range(1, paginator_obj.num_pages+1):
                    for state in paginator_obj.page(page):
                        states_list.append(state.name)
            elif header == "Country":
                for page in range(1, paginator_obj.num_pages+1):
                    for state in paginator_obj.page(page):
                        countries_list.append(state.country.name)
            elif header == "Number of Cities":
                for page in range(1, paginator_obj.num_pages+1):
                    for state in paginator_obj.page(page):
                        cities_list.append(state.num_cities)
    else:

        for page in range(1, paginator_obj.num_pages+1):
            for state in paginator_obj.page(page):
                states_list.append(state.name)
                cities_list.append(state.num_cities)
                countries_list.append(state.country.name)
    return headers_here, states_list, countries_list,cities_list

@login_required(login_url='login')
def all_states(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        STATE_NAME_SYNTAX_ERROR

    )
    paginator = Paginator(states, 5)
    searchManObj = SearchMan("State")
    report_man = ReportMan()
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests

        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = State.objects.annotate(num_cities=Count('country')).filter(
                name=search_message).order_by('-num_cities')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter category  first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')
        searchManObj.setPaginator(all_states)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')
        searchManObj.setPaginator(all_states)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("State")
        headers.append("Country")
        headers.append("Number of Cities")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, states_list, countries_list , cities_list = prepare_selected_query_state(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(states_list) > 0:
                    constructor.update({"state": states_list})
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                if len(cities_list) > 0:
                    constructor.update({"num_cities": cities_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_States',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, states_list, countries_list , cities_list = prepare_selected_query_state(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_States',
                                                                                  headers, state=states_list,
                                                                                  country=countries_list,num_cities=cities_list
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = searchManObj.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, states_list, countries_list , cities_list = prepare_query_state(query, headers=headers)
                if len(states_list) > 0:
                    constructor.update({"state": states_list})
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                if len(cities_list) > 0:
                    constructor.update({"num_cities": cities_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_States',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, states_list, countries_list,cities_list = prepare_query_state(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_States',
                                                                                  headers,state=states_list,
                                                                                  num_cities=cities_list,
                                                                                  country=countries_list
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = searchManObj.getPaginator()
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
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "state_error": STATE_NAME_SYNTAX_ERROR,
                      }
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