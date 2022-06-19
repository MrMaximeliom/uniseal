from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import redirect

from Util.utils import (SearchMan,
                        createExelFile,
                        ReportMan,
                        delete_temp_folder,
                        get_selected_pages,
                        prepare_default_query,
                        prepare_selected_query)
from apps.category.models import Category
from apps.common_code.views import BaseListView

categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
report_man = ReportMan()

class CategoryListView(BaseListView):
    def get(self, request, *args, **kwargs):
        from Util.search_form_strings import (
            EMPTY_SEARCH_PHRASE,
            CLEAR_SEARCH_TIP,
            CREATE_REPORT_TIP

        )
        search_result = ''
        ssearch_object = SearchMan(self.model_name)
        queryset = ssearch_object.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            instances = ssearch_object.get_queryset()
            ssearch_object.setPaginator(instances)
            ssearch_object.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = ssearch_object.getPaginator()
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
            'search': ssearch_object.getSearch(),
            'search_result': search_result,
            'search_phrase': ssearch_object.getSearchPhrase(),
            'search_option': ssearch_object.getSearchOption(),
            'search_error': ssearch_object.getSearchError(),
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
        search_object = SearchMan(self.model_name)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        print(request.POST)
        if  'clear' not in request.POST and 'createExcel' not in request.POST:
            search_object.setSearch(True)
            if request.POST.get('search_phrase') is not None:
                print("hi1")
                print(request.POST.get('search_phrase'))
                search_message = request.POST.get('search_phrase')
                search_result = Category.objects.annotate(num_products=Count('product')).filter(
                    name=search_message).order_by('-num_products')
                search_object.setPaginator(search_result)
                search_object.setSearchPhrase(search_message)
                search_object.setSearchOption('Category')
                search_object.setSearchError(False)
            else:
                messages.error(request,
                               "Please enter category  first!")
                search_object.setSearchError(True)



        if  request.POST.get('clear') == 'clear':
            print("hi2")
            instances = search_object.get_queryset()
            search_object.setPaginator(instances)
            search_object.setSearch(False)
        if request.method == "POST" and request.POST.get('createExcel') == 'done':
            headers = []
            headers.append("name")
            headers.append("number_of_products")
            # create report functionality
            # setting all data as default behaviour
            if request.POST.get('pages_collector') != 'none' and len(request.POST.get('pages_collector')) > 0:
                # get requested pages from the paginator of original page
                selected_pages = get_selected_pages(request.POST.get('pages_collector'))
                query = search_object.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_selected_query(search_object.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                      headers, **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


                else:
                    headers = ["name", "number_of_products"]
                    constructor = prepare_selected_query(search_object.get_queryset(),headers,selected_pages,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                      headers,
                                                                                      **constructor
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
                query = search_object.getPaginator()
                if len(headers) > 0:
                    constructor = prepare_default_query(search_object.get_queryset(),headers,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                      headers, **constructor)
                    if status:

                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created ")

                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

                else:
                    headers = ["name","number_of_products"]
                    constructor = prepare_default_query(search_object.get_queryset(),headers,query)
                    status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                      headers,
                                                                                      **constructor)
                    if status:
                        request.session['temp_dir'] = 'delete man!'
                        messages.success(request, f"Report Successfully Created")
                        return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                    else:
                        messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))

        else:
            page = None
        try:
            paginator = search_object.getPaginator()
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
                'search': search_object.getSearch(),
                'search_result': search_result,
                'search_phrase': search_object.getSearchPhrase(),
                'search_option': search_object.getSearchOption(),
                'search_error': search_object.getSearchError(),
                'create_report_tip': CREATE_REPORT_TIP,
                'clear_search_tip': CLEAR_SEARCH_TIP,
                'data_js': {
                    "empty_search_phrase": EMPTY_SEARCH_PHRASE,

                }
            }
        return super().get(request)



