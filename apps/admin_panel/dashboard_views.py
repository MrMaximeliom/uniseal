from django.views.generic import ListView
from Util.search_form_strings import (CLEAR_SEARCH_TIP ,
    PRODUCTS_VIEWS_TITLE,SEARCH_PRODUCTS_VIEWS_TIP,PRODUCTS_PAGE_VIEWS_TITLE,
                                      EMPTY_SEARCH_PHRASE_PRODUCTS_VIEWS,EMPTY_SEARCH_PHRASE_PRODUCTS_PAGE_VIEWS)
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import ManageProducts,ManageProductsPage
from django.db.models import Count
from django.db.models import Q
#     ,ManageBrochures,ManageSellingPoints,ManageProjects,ManageCarts,ManageSolution
# from .forms import (ManageBrochuresForm,ManageProductsForm,
#                     ManageCartsForm,ManageProductsPageForm
# ,ManageProjectsForm,ManageSellingPointsForm,ManageSolutionForm)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



class ViewsReportsListView(ListView):
    model = ManageProducts
    template_name = "admin_panel/products_views.html"
    active_flag = 'products_views'
    searchManObj = SearchMan("ManageProducts")
    search_result = None
    report_man = ReportMan()
    title = PRODUCTS_VIEWS_TITLE

    def get_count(self,flag_count):
        query =  self.get_queryset()
        list_count = []
        for record in query:
            list_count.append(record[flag_count])
        return list_count
    def get_queryset(self):
        return ManageProducts.objects.values('product__name').annotate(num_users=Count('product__name')).order_by('-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageProducts.objects.values('product__name').annotate(num_users=Count('product__name')).filter(
                Q(product__name__icontains=search_message)).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Product Name')
            self.searchManObj.setSearchError(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProducts = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProducts = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProducts = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'products_views_list': manageProducts,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_products_views_tip': SEARCH_PRODUCTS_VIEWS_TIP,
            'current_page': page,
            'title':self.title,
            'data_js': {
                "num_users": self.get_count('num_users'),
                'products_names': self.get_count('product__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PRODUCTS_VIEWS,
            }
        }
        return super().get(request)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            manageProducts = ManageProducts.objects.values('product__name').annotate(num_users=Count('product__name')).order_by('num_users')
            self.searchManObj.setPaginator(manageProducts)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProducts = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProducts = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProducts = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'products_views_list': manageProducts,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_products_views_tip': SEARCH_PRODUCTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            # 'num_users':self.get_count('num_users'),

            'data_js': {
                "num_users": self.get_count('num_users'),
                'products_names': self.get_count('product__name'),
                "empty_search_phrase":EMPTY_SEARCH_PHRASE_PRODUCTS_VIEWS,
            }
        }
        return super().get(request)

class ProductsPageViews(ListView):
    # import datetime
    # ManageProductsPage.objects.filter(
    #     visit_date_time__range=(datetime.datetime(2021, 1, 10, 11, 49, 25, 389820, tzinfo=datetime.timezone.utc),
    #     datetime.datetime(2022, 2, 20, 11, 49, 25, 389820, tzinfo=datetime.timezone.utc)))
    model = ManageProductsPage
    template_name = "admin_panel/product_page_views.html"
    active_flag = 'products_page_views'
    searchManObj = SearchMan("ManageProductsPage")
    search_result = None
    report_man = ReportMan()
    title = PRODUCTS_PAGE_VIEWS_TITLE


    def get_queryset(self):
        return ManageProductsPage.objects.all().order_by('-visit_date_time')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase_date') != '':
            search_message = request.POST.get('search_phrase_date')
            self.search_result = ManageProductsPage.objects.filter(
                Q(visit_date_time=search_message)).order_by('-visit_date_time')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Visiting Date')
            self.searchManObj.setSearchError(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProductsPage = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProductsPage = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProductsPage = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'products_views_list': manageProductsPage,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_products_views_tip': SEARCH_PRODUCTS_VIEWS_TIP,
            'current_page': page,
            'title':self.title,
            'data_js': {

                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PRODUCTS_PAGE_VIEWS,
            }

        }
        return super().get(request)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'temp_dir' in request.session:
            # deleting temp dir in GET requests
            if request.session['temp_dir'] != '':
                delete_temp_folder()
        if 'page' not in request.GET:
            manageProductsPage = self.get_queryset()
            self.searchManObj.setPaginator(manageProductsPage)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProductsPage = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProductsPage = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProductsPage = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'products_views_list': manageProductsPage,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_products_views_tip': SEARCH_PRODUCTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {

                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PRODUCTS_PAGE_VIEWS,
            }
        }
        return super().get(request)

