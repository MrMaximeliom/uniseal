from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import  redirect
from Util.utils import (SearchMan, createExelFile,
                        ReportMan, delete_temp_folder,
                        get_fields_names_for_report_file,
                        get_selected_pages,
                        prepare_selected_query,
                        prepare_default_query)
from apps.address.models import Area
from apps.common_code.views import BaseListView
search_man_areas = SearchMan("Area")
report_man_areas = ReportMan()



class AreaListView(BaseListView):
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
                search_result = Area.objects.filter(
                    city__name__icontains=search_message).order_by('id')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('City')
                searchManObj.setSearchError(False)
            elif request.POST.get('search_options') == 'area':
                search_message = request.POST.get('search_phrase')
                search_result = Area.objects.filter(
                    name__icontains=search_message).order_by('id')
                searchManObj.setPaginator(search_result)
                searchManObj.setSearchPhrase(search_message)
                searchManObj.setSearchOption('Area')
                searchManObj.setSearchError(False)
            else:
                messages.error(request,
                               "Please enter city name first!")
                searchManObj.setSearchError(True)
            # check if user request to create a report file
        if  request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name")
            headers.append("city")
            # create report functionality
            # check if user has selected pages to create the report file or not
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages selected by the user
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                # get the paginator object
                query = search_man_areas.getPaginator()
                # check if headers length is greater than 0
                if len(headers) > 0:
                    constructor = prepare_selected_query(search_man_areas.get_queryset(), headers, selected_pages, query)
                    status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                                  headers,
                                                                                                  **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man_areas.filePath),
                                        str(report_man_areas.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = get_fields_names_for_report_file(Area,Area.get_not_wanted_fields_names_in_report_file())
                    constructor = prepare_selected_query(search_man_areas.get_queryset(),
                                                         headers, selected_pages, query)
                    status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                                  headers,
                                                                                                  **constructor
                                                                                                  )
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man_areas.filePath),
                                        str(report_man_areas.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
                # get the original query of page and then structure the data
            else:
                query = search_man_areas.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_default_query(search_man_areas.get_queryset(), headers, query)
                    status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                                  headers,
                                                                                                  **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man_areas.filePath),
                                        str(report_man_areas.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    constructor = prepare_default_query(search_man_areas.get_queryset(), headers, query)
                    status, report_man_areas.filePath, report_man_areas.fileName = createExelFile('Report_For_Areas',
                                                                                                  headers,
                                                                                                  **constructor
                                                                                                  )
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man_areas.filePath),
                                        str(report_man_areas.fileName))
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
# ends here
areas = Area.objects.annotate(num=Count('city')).order_by('-num')

