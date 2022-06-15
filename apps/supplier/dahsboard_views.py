from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
from .models import Supplier

suppliers = Supplier.objects.all().order_by("id")
searchManObj = SearchMan("Supplier")
report_man = ReportMan()
from apps.common_code.views import BaseListView


class SuppliersListView(BaseListView):
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
            search_message = request.POST.get('search_phrase')
            search_result = Supplier.objects.filter(name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Supplier Name')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter supplier name first!")
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

def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    link_list = []
    supplier_list = []
    headers_here = ["Supplier Name", "Supplier Website"]
    if headers is not None:
        print("in headers section of selected query")
        headers_here = headers
        for header in headers_here:
            if header == "Supplier Name":
                for page in selected_pages:
                    for supplier in paginator_obj.page(page):
                        supplier_list.append(supplier.name)
            elif header == "Supplier Website":
                print("here in supplier website")
                for page in selected_pages:
                    print("in for loop for supplier website")
                    for supplier in paginator_obj.page(page):
                        print("appending supplier links")
                        link_list.append(supplier.link)
    else:
        print("in else section of selected query")
        for page in range(1, paginator_obj.num_pages+1):
            for supplier in paginator_obj.page(page):
                link_list.append(supplier.link)
                supplier_list.append(supplier.name)


    return headers_here, supplier_list , link_list
def prepare_query(paginator_obj,headers=None):
    supplier_list = []
    link_list = []
    headers_here = ["Supplier Name","Supplier Website"]
    if headers is not None:
        print("in headers section of prepare query")
        headers_here = headers
        for header in headers_here:
            if header == "Supplier Name":
                for page in range(1, paginator_obj.num_pages+1):
                    for supplier in paginator_obj.page(page):
                        supplier_list.append(supplier.name)
            elif header == "Supplier Website":
                for page in range(1, paginator_obj.num_pages+1):
                    for supplier in paginator_obj.page(page):
                        link_list.append(supplier.link)
    else:
        print("in else section of prepare query")
        for page in range(1, paginator_obj.num_pages+1):
            for supplier in paginator_obj.page(page):
                supplier_list.append(supplier.name)
                link_list.append(supplier.link)
    return headers_here, supplier_list, link_list
@staff_member_required(login_url='login')
def all_suppliers(request):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    paginator = Paginator(suppliers, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    SUPPLIER_NAME_SYNTAX_ERROR,
    CREATE_REPORT_TIP,
    CLEAR_SEARCH_TIP,
    SEARCH_SUPPLIERS_TIP,

    )
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Supplier.objects.filter(name=search_message).order_by('id')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Supplier Name')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter supplier name first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET  and not searchManObj.getSearch():
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_suppliers = Supplier.objects.all().order_by("id")
        searchManObj.setPaginator(all_suppliers)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Supplier Name")
        headers.append("Supplier Website")
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none':
            print("pages collector is not none")
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                print('in page selectors')
                if item != ",":
                    selected_pages.append(item)
            print("selected pages are: ",selected_pages)
            if len(headers) > 0:
                print("headers hase value with collector is not none")
                constructor = {}
                headers, supplier ,link = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                print("suppliers: ",supplier,"\n","links: ",link)
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(link) > 0:
                    constructor.update({"link": link})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Suppliers',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Supplier Name", "Supplier Website"]
                headers, supplier , link = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Suppliers',
                                                                                  headers, supplier=supplier,
                                                                                  link=link
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
            if len(headers) > 0:
                constructor = {}
                headers,  supplier , link = prepare_query(query,headers=headers)
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(link) > 0:
                    constructor.update({"link": link})
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Suppliers',
                                                                                  headers, **constructor)
                if status:
                   # request.session['temp_dir'] = report_man.tempDir
                   request.session['temp_dir'] = 'delete man!'
                   messages.success(request, f"Report Successfully Created ")
                   # return redirect('download_file',filepath=filepath,filename=filename)

                   return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers, supplier,link = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile( 'Report_For_Suppliers',
                                                                                  headers,supplier=supplier,
                                                                                  link=link)
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
        paginator = searchManObj.getPaginator()
        supplier_data = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        supplier_data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        supplier_data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'supplier/all_suppliers.html',
                  {
                      'title': _('All Suppliers'),
                      'all_suppliers': 'active',
                      'suppliers':'active',
                      'all_suppliers_data': supplier_data,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'create_report_tip': CREATE_REPORT_TIP,
                      'clear_search_tip': CLEAR_SEARCH_TIP,
                      'search_suppliers_tip': SEARCH_SUPPLIERS_TIP,

                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )
