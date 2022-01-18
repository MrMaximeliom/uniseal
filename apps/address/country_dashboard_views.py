from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from Util.utils import rand_slug
from apps.address.models import Country

# countries = Country.objects.all()
countries = Country.objects.all().order_by('id')


def prepare_selected_query_country(selected_pages, paginator_obj, headers=None):
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
        for page in range(1, paginator_obj.num_pages + 1):
            for country in paginator_obj.page(page):
                country_list.append(country.name)
    return headers_here, country_list


def prepare_query_country(paginator_obj, headers=None):
    countries = []
    headers_here = ["Country"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Country":
                for page in range(1, paginator_obj.num_pages + 1):
                    for country in paginator_obj.page(page):
                        countries.append(country.name)
    else:
        for page in range(1, paginator_obj.num_pages + 1):
            for country in paginator_obj.page(page):
                countries.append(country.name)
    return headers_here, countries

search_man_countries = SearchMan("Country")
report_man_countries = ReportMan()
@staff_member_required(login_url='login')
def all_countries(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''

    paginator = Paginator(countries, 5)
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_countries.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            search_man_countries.setPaginator(search_result)
            search_man_countries.setSearchPhrase(search_message)
            search_man_countries.setSearchOption('Country')
            search_man_countries.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            search_man_countries.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not search_man_countries.getSearch():
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = search_man_countries.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages,
                                                                         paginator_obj=query,
                                                                         headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Country"]
                headers, countries_list = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = search_man_countries.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_countries.getPaginator()
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
                      'address': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_countries.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_countries.getSearchPhrase(),
                      'search_option': search_man_countries.getSearchOption(),
                      'search_error': search_man_countries.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
                  }
                  )


@staff_member_required(login_url='login')
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
        'form': form,
        'address': 'active',
    }

    return render(request, 'address/add_countries.html', context)


@staff_member_required(login_url='login')
def delete_countries(request):
    paginator = Paginator(countries, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_countries.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            search_man_countries.setPaginator(search_result)
            search_man_countries.setSearchPhrase(search_message)
            search_man_countries.setSearchOption('Country')
            search_man_countries.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            search_man_countries.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not search_man_countries.getSearch():
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = search_man_countries.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages,
                                                                         paginator_obj=query,
                                                                         headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, countries_list = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = search_man_countries.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_countries.getPaginator()
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
                      'address': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_countries.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_countries.getSearchPhrase(),
                      'search_option': search_man_countries.getSearchOption(),
                      'search_error': search_man_countries.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
                  }
                  )


@staff_member_required(login_url='login')
def edit_countries(request):
    paginator = Paginator(countries, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        COUNTRY_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_countries.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Country.objects.filter(
                name=search_message).order_by('id')
            search_man_countries.setPaginator(search_result)
            search_man_countries.setSearchPhrase(search_message)
            search_man_countries.setSearchOption('Country')
            search_man_countries.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter country name first!")
            search_man_countries.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not search_man_countries.getSearch():
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_countries = Country.objects.all().order_by('id')
        search_man_countries.setPaginator(all_countries)
        search_man_countries.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Country")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = search_man_countries.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, countries_list = prepare_selected_query_country(selected_pages=selected_pages,
                                                                         paginator_obj=query,
                                                                         headers=headers)
                if len(countries_list) > 0:
                    constructor.update({"country": countries_list})
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, countries_list = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,

                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = search_man_countries.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, countries_list = prepare_query_country(query, headers=headers)
                if len(countries_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": countries_list})

                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile('Report_For_Countries',
                                                                                  headers, category=countries_list,
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_countries.filePath), str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter

        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_countries.getPaginator()
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
                      'address': 'active',
                      'all_countries_data': countries_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_countries.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_countries.getSearchPhrase(),
                      'search_option': search_man_countries.getSearchOption(),
                      'search_error': search_man_countries.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "country_error": COUNTRY_NAME_SYNTAX_ERROR,
                      }
                  }
                  )

@staff_member_required(login_url='login')
def edit_country(request, slug):
    from .models import Country
    from .forms import CountryForm
    # fetch the object related to passed id
    obj = get_object_or_404(Country, slug=slug)

    # pass the object as instance in form
    country_form = CountryForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if country_form.is_valid():
        country_form.save()
        name = country_form.cleaned_data.get('name')
        messages.success(request, f"Country {name} Updated")
    else:
        for field, items in country_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))

    context = {
        'title': _('Edit Country'),
        'edit_countries': 'active',
        'form': country_form,
        'country': obj,
        'address': 'active',
    }
    return render(request, 'address/edit_country.html', context)

@staff_member_required(login_url='login')

def confirm_country_delete(request, id):
    from .models import Country
    obj = get_object_or_404(Country, id=id)
    try:
        obj.delete()
        messages.success(request, f"Country {obj.name} deleted successfully")
    except:
        messages.error(request, f"Country {obj.name} was not deleted , please try again!")

    return redirect('deleteCountries')
