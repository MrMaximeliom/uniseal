from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from apps.address.models import City
# new code starts here
from apps.common_code.views import BaseListView


class CityListView(BaseListView):
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
    def post(self,request,*args,**kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        searchManObj = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if  'clear' not in request.POST and 'createExcel' not in request.POST:
            searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'city':
                search_message = request.POST.get('search_phrase')
                search_result = City.objects.annotate(num_areas=Count('area')).filter(
                    name__icontains=search_message).order_by('-num_areas')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('City')
                searchManObj.setSearchError(False)

            elif request.POST.get('search_options') == 'state':
                search_message = request.POST.get('search_phrase')
                search_result = City.objects.annotate(num_areas=Count('area')).filter(
                    state__name__icontains=search_message).order_by('-num_areas')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('State')
                searchManObj.setSearchError(False)

            else:
                messages.error(request,
                               "Please enter city name first!")
                searchManObj.setSearchError(True)

        if  request.POST.get('clear') == 'clear':
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
# ends here
cities = City.objects.all().order_by('id')

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
@staff_member_required(login_url='login')
def all_cities(request):
    paginator = Paginator(cities, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CITY_NAME_SYNTAX_ERROR,
    STATE_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_cities.setSearch(True)
        if request.POST.get('search_options') == 'city':
            search_message = request.POST.get('search_phrase')
            search_result = City.objects.annotate(num_areas=Count('area')).filter(
                name__icontains=search_message).order_by('-num_areas')
            search_man_cities.setPaginator(search_result)
            search_man_cities.setSearchPhrase(search_message)
            search_man_cities.setSearchOption('City')
            search_man_cities.setSearchError(False)

        elif request.POST.get('search_options') == 'state':
            search_message = request.POST.get('search_phrase')
            search_result = City.objects.annotate(num_areas=Count('area')).filter(
                state__name__icontains=search_message).order_by('-num_areas')
            search_man_cities.setPaginator(search_result)
            search_man_cities.setSearchPhrase(search_message)
            search_man_cities.setSearchOption('State')
            search_man_cities.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter city name first!")
            search_man_cities.setSearchError(True)

    if request.method == "GET" and 'page' not in request.GET and not search_man_cities.getSearch():
        all_cities = City.objects.annotate(num_areas=Count('area')).order_by('-num_areas')
        search_man_cities.setPaginator(all_cities)
        search_man_cities.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_cities = City.objects.annotate(num_areas=Count('area')).order_by('-num_areas')
        search_man_cities.setPaginator(all_cities)
        search_man_cities.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("City")
        headers.append("State")
        headers.append("Number of Areas")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
            # get requested pages from the paginator of original page
            selected_pages = []
            query = search_man_cities.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, states_list,cities_list,areas_list = prepare_selected_query_city(selected_pages=selected_pages,
                                                                         paginator_obj=query,
                                                                         headers=headers)
                if len(states_list) > 0:
                    constructor.update({"state": states_list})
                if len(cities_list) > 0:
                    constructor.update({"city": cities_list})
                if len(areas_list) > 0:
                    constructor.update({"num_areas": areas_list})
                status, report_man_cities.filePath, report_man_cities.fileName = createExelFile('Report_For_Cities',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man_cities.filePath), str(report_man_cities.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, states_list,cities_list,areas_list = prepare_selected_query_city(
                    selected_pages, query, headers)
                status, report_man_cities.filePath, report_man_cities.fileName = createExelFile('Report_For_Cities',
                                                             headers, state=states_list, city=cities_list,area=areas_list
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'

                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_cities.filePath), str(report_man_cities.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            print("pages collector is none")
            query = search_man_cities.getPaginator()
            print("query in major if is: ", query.num_pages)
            if len(headers) > 0:
                print("in major if")
                constructor = {}
                headers, states_list,cities_list,areas_list = prepare_query_city(query, headers=headers)
                if len(states_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"state": states_list})
                if len(cities_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"city": cities_list})
                if len(areas_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"area": areas_list})

                status, report_man_cities.filePath, report_man_cities.fileName = createExelFile('Report_For_Cities',
                                                                                  headers, **constructor)
                if status:

                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man_cities.filePath), str(report_man_cities.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                print("in major else")
                headers, states_list,cities_list,areas_list = prepare_query_city(query)
                status, report_man_cities.filePath, report_man_cities.fileName = createExelFile('Report_For_Cities',
                                                                                  headers, state=states_list,
                                                                                                      city=cities_list,area=areas_list
                                                                                  )
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created")
                    return redirect('downloadReport', str(report_man_cities.filePath), str(report_man_cities.fileName))
                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_cities.getPaginator()
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
                      'address': 'active',
                      'all_cities_data': cities_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_cities.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_cities.getSearchPhrase(),
                      'search_option': search_man_cities.getSearchOption(),
                      'search_error': search_man_cities.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "city_error": CITY_NAME_SYNTAX_ERROR,
                          "state_error": STATE_NAME_SYNTAX_ERROR
                      }
                  }
                  )

