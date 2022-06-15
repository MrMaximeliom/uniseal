from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from apps.address.models import Country

countries = Country.objects.all().order_by('id')

from apps.common_code.views import BaseListView
class CountryListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            }
        }
        return super().get(request)

    def post(self, request, *args, **kwargs):
        from apps.address.models import Country
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_phrase') != '':
                print("searching for countries")
                search_message = request.POST.get('search_phrase')
                search_result = Country.objects.filter(
                    name__icontains=search_message).order_by('id')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Country')
                searchManObj.setSearchError(False)

            else:
                messages.error(request,
                               "Please enter country name first!")
                searchManObj.setSearchError(True)

        if request.POST.get('clear') == 'clear':
            instances = searchManObj.get_queryset()
            searchManObj.setPaginator(instances)
            searchManObj.setSearch(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = searchManObj.getPaginator()
            instances = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            instances = paginator.page(1)
            page = 1

        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            instances = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'object_list': instances,
            self.main_active_flag: 'active',
            self.active_flag: "active",
            'current_page': page,
            'title': self.title,
            'search': searchManObj.getSearch(),
            'search_result': search_result,
            'search_phrase': searchManObj.getSearchPhrase(),
            'search_option': searchManObj.getSearchOption(),
            'search_error': searchManObj.getSearchError(),
            'create_report_tip': CREATE_REPORT_TIP,
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'data_js': {
                "empty_search_phrase": EMPTY_SEARCH_PHRASE,

            }
        }
        return super().get(request)


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
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile(
                    'Report_For_Countries',
                    headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_countries.filePath),
                                    str(report_man_countries.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Country"]
                headers, countries_list = prepare_selected_query_country(
                    selected_pages, query, headers)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile(
                    'Report_For_Countries',
                    headers, category=countries_list,

                    )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath),
                                    str(report_man_countries.fileName))

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

                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile(
                    'Report_For_Countries',
                    headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_countries.filePath),
                                    str(report_man_countries.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, countries_list = prepare_query_country(query)
                status, report_man_countries.filePath, report_man_countries.fileName = createExelFile(
                    'Report_For_Countries',
                    headers, category=countries_list,
                    )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_countries.filePath),
                                    str(report_man_countries.fileName))
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
