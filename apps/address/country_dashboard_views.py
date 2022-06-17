from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from Util.utils import SearchMan, createExelFile, ReportMan, \
    delete_temp_folder,get_selected_pages,prepare_selected_query,prepare_default_query
from apps.address.models import Country

countries = Country.objects.all().order_by('id')
report_man = ReportMan()

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
        if request.method == "POST" and request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name")
            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = searchManObj.getPaginator()
                print("original values: ", request.POST.get('pages_collector'))
                if len(headers) > 0:

                    constructor = prepare_selected_query(searchManObj.get_queryset(),headers,selected_pages,query)
                    # if len(countries_list) > 0:
                    #     constructor.update({"country": countries_list})
                    status, report_man.filePath, report_man.fileName = createExelFile(
                        'Report_For_Countries',
                        headers, **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath),
                                        str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = ["name"]
                    constructor = prepare_default_query(searchManObj.get_queryset(),
                         query, headers)
                    status, report_man.filePath, report_man.fileName =  createExelFile('Report_For_Users', headers,
                                                                                    **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'

                        messages.success(request, f"Report Successfully Created ")
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man.filePath),
                                        str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
                # get the original query of page and then structure the data
            else:
                query = searchManObj.getPaginator()
                if len(headers) > 0:
                    constructor  = prepare_default_query(searchManObj.get_queryset(),headers, query)
                    print(constructor)
                    # if len(countries_list) > 0:
                    #     print("application list is bigger than 0")
                    #     constructor.update({"category": countries_list})

                    status, report_man.filePath, report_man.fileName = createExelFile(
                        'Report_For_Countries',
                        headers, **constructor)
                    if status:

                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        # return redirect('download_file',filepath=filepath,filename=filename)

                        return redirect('downloadReport', str(report_man.filePath),
                                        str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:

                    constructor  = prepare_default_query(searchManObj.get_queryset(),headers, query)
                    status, report_man.filePath, report_man.fileName = createExelFile(
                        'Report_For_Countries',
                        headers, **constructor,
                    )
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man.filePath),
                                        str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

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

