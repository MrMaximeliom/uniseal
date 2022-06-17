from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from Util.utils import (SearchMan, createExelFile,
                        ReportMan,
                        delete_temp_folder,
                        get_fields_names_for_report_file,
                        get_selected_pages,
                        prepare_selected_query,
                        prepare_default_query
                        )
from Util.utils import rand_slug
from apps.address.models import State

states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')

from apps.common_code.views import BaseListView


class StateListView(BaseListView):
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
            if request.POST.get('search_options') == 'state':
                search_message = request.POST.get('search_phrase')
                search_result = State.objects.annotate(num_cities=Count('country')).filter(
                    name__icontains=search_message).order_by('-num_cities')
                print("search results are: ", search_result)
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('State')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'country':
                search_message = request.POST.get('search_phrase')
                search_result = State.objects.annotate(num_cities=Count('country')).filter(
                    country__name__icontains=search_message).order_by('-num_cities')
                print("search results are: ", search_result)
                query_mano = search_result
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Country')
                searchManObj.setSearchError(False)

            else:
                messages.error(request,
                               "Please enter category  first!")
                searchManObj.setSearchError(True)
        if request.method == "POST" and request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name")
            headers.append("country")
            headers.append("number_of_cities")
            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = search_man_states.getPaginator()
                if len(headers) > 0:
                    pago = search_man_states.getPaginator()
                    for page in selected_pages:
                        for state in pago.page(page):
                            print(state.name)
                    constructor = prepare_selected_query(search_man_states.get_queryset(),headers,selected_pages,query)
                    status, report_man_states.filePath, report_man_states.fileName = createExelFile('Report_For_States',
                                                                                                    headers,
                                                                                                    **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man_states.filePath),
                                        str(report_man_states.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    # set default headers if the user has not selected any
                    headers = get_fields_names_for_report_file(State, State.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_selected_query(search_man_states.get_queryset(),headers,selected_pages,query)
                    status, report_man_states.filePath, report_man_states.fileName = createExelFile('Report_For_States',
                                                                                                    headers,
                                                                                                    **constructor
                                                                                                    )
                    if status:
                        request.session['temp_dir'] = 'delete man!'

                        messages.success(request, f"Report Successfully Created ")
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man_states.filePath),
                                        str(report_man_states.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
                # get the original query of page and then structure the data
            else:
                print("pages collector is none")
                query = search_man_states.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_default_query(search_man_states.get_queryset(),headers,query)
                    status, report_man_states.filePath, report_man_states.fileName = createExelFile('Report_For_States',
                                                                                                    headers,
                                                                                                    **constructor)
                    if status:

                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man_states.filePath),
                                        str(report_man_states.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    # set default headers if the user has not selected any
                    headers = get_fields_names_for_report_file(State,
                                                               State.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_default_query(search_man_states.get_queryset(),headers,query)
                    status, report_man_states.filePath, report_man_states.fileName = createExelFile('Report_For_States',
                                                                                                    headers,
                                                                                                    **constructor
                                                                                                    )
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man_states.filePath),
                                        str(report_man_states.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

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



search_man_states = SearchMan("State")
report_man_states = ReportMan()
@staff_member_required(login_url='login')
def all_states(request):
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        STATE_NAME_SYNTAX_ERROR,
    COUNTRY_NAME_SYNTAX_ERROR

    )
    paginator = Paginator(states, 5)

    search_result = ''
    query_mano = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests

        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        search_man_states.setSearch(True)
        if request.POST.get('search_options') == 'state':
            search_message = request.POST.get('search_phrase')
            search_result = State.objects.annotate(num_cities=Count('country')).filter(
                name__icontains=search_message).order_by('-num_cities')
            print("search results are: ", search_result)
            query_mano = search_result
            search_man_states.setPaginator(search_result)
            search_man_states.setSearchPhrase(search_message)
            search_man_states.setSearchOption('State')
            search_man_states.setSearchError(False)
        elif request.POST.get('search_options') == 'country':
            search_message = request.POST.get('search_phrase')
            search_result = State.objects.annotate(num_cities=Count('country')).filter(
                country__name__icontains=search_message).order_by('-num_cities')
            print("search results are: ", search_result)
            query_mano = search_result
            search_man_states.setPaginator(search_result)
            search_man_states.setSearchPhrase(search_message)
            search_man_states.setSearchOption('Country')
            search_man_states.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter category  first!")
            search_man_states.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        print("second if")
        all_states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')
        print(all_states)
        search_man_states.setPaginator(all_states)
        search_man_states.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')
        search_man_states.setPaginator(all_states)
        search_man_states.setSearch(False)

    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        # Create a page object for the current page.
        paginator = search_man_states.getPaginator()
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
                      'address': 'active',
                      'all_states_data': states_paginator,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': search_man_states.getSearch(),
                      'search_result': search_result,
                      'search_phrase': search_man_states.getSearchPhrase(),
                      'search_option': search_man_states.getSearchOption(),
                      'search_error': search_man_states.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "state_error": STATE_NAME_SYNTAX_ERROR,
                          "country_error":COUNTRY_NAME_SYNTAX_ERROR
                      }
                  }
                  )


@staff_member_required(login_url='login')
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
        'form': form,
        'address': 'active',
    }

    return render(request, 'address/add_states.html', context)


