from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, createExelFile, ReportMan, delete_temp_folder
# Views for dashboard
from apps.category.models import Category
# new code starts here
from apps.common_code.views import BaseListView


class CategoryListView(BaseListView):
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
        if request.POST.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            search_result = Category.objects.annotate(num_products=Count('product')).filter(
                name=search_message).order_by('-num_products')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter category  first!")
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
categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
searchManObj = SearchMan("Category")
report_man = ReportMan()
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    categories_list = []
    products_list = []
    headers_here = ["Category", "Number of Products"]
    if headers is not None:
        print("in selected query headers are not none")
        headers_here = headers
        for header in headers_here:
            if header == "Category":
                for page in selected_pages:
                    for category in paginator_obj.page(page):
                        categories_list.append(category.name)
            elif header == "Number of Products":
                for page in selected_pages:
                    print("in for loop for supplier website")
                    for category in paginator_obj.page(page):
                        products_list.append(category.num_products)
    else:
        for page in range(1, paginator_obj.num_pages+1):
            for category in paginator_obj.page(page):
                products_list.append(category.num_products)
                categories_list.append(category.name)
    return headers_here, categories_list,products_list
def prepare_query(paginator_obj,headers=None):
    categories_list = []
    products_list = []
    headers_here = ["Category","Number of Products"]
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Category":
                for page in range(1, paginator_obj.num_pages+1):
                    for category in paginator_obj.page(page):
                        categories_list.append(category.name)
            elif header == "Number of Products":
                for page in range(1, paginator_obj.num_pages+1):

                    for category in paginator_obj.page(page):
                        products_list.append(category.num_products)
    else:

        for page in range(1, paginator_obj.num_pages+1):
            for category in paginator_obj.page(page):
                categories_list.append(category.name)
                products_list.append(category.num_products)
    return headers_here, categories_list, products_list
@staff_member_required(login_url='login')
def all_categories(request):
    paginator = Paginator(categories, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        CATEGORY_NAME_SYNTAX_ERROR

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
            search_result = Category.objects.annotate(num_products=Count('product')).filter(
                name=search_message).order_by('-num_products')
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)

        else:
            messages.error(request,
                           "Please enter category  first!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
        searchManObj.setPaginator(all_categories)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
        searchManObj.setPaginator(all_categories)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Category")
        headers.append("Number of Products")
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
                headers, categories_list, product_list = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(categories_list) > 0:
                    constructor.update({"category": categories_list})
                if len(product_list) > 0:
                    constructor.update({"num_products": product_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                  headers, **constructor)
                if status:
                    request.session['temp_dir'] = 'delete man!'
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers = ["Category", "Number of Products"]
                headers, categories_list, product_list = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                  headers, category=categories_list,
                                                                                  num_products=product_list
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
                headers, categories_list, product_list = prepare_query(query, headers=headers)
                if len(categories_list) > 0:
                    print("application list is bigger than 0")
                    constructor.update({"category": categories_list})
                if len(product_list) > 0:
                    print("project list is bigger than 0")
                    constructor.update({"num_products": product_list})
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
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
                headers, categories_list, product_list = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile('Report_For_Categories',
                                                                                  headers,category=categories_list,
                                                                                  num_products=product_list)
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
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        categories_paginator = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        categories_paginator = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'category/all_categories.html',
                  {
                      'title': _('All Product Categories'),
                      'all_categories': 'active',
                      'categories':'active',
                      'all_categories_data': categories_paginator,
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
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                      }
                  }
                  )

