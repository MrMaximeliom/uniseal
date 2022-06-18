from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import  redirect
from Util.utils import (SearchMan, createExelFile,
                        ReportMan,
                        delete_temp_folder,
                        get_fields_names_for_report_file,
                        get_selected_pages,
                        prepare_selected_query,
                        prepare_default_query
                        )
from apps.address.models import State

states = State.objects.annotate(num_cities=Count('country')).order_by('-num_cities')

from apps.common_code.views import BaseListView
search_man_states = SearchMan("State")
report_man_states = ReportMan()

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




