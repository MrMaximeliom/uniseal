from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.db.models import Q
from django.views.generic import ListView

from Util.search_form_strings import (CLEAR_SEARCH_TIP,
                                      PRODUCTS_VIEWS_TITLE, SEARCH_PRODUCTS_VIEWS_TIP, PRODUCTS_PAGE_VIEWS_TITLE,
                                      EMPTY_SEARCH_PHRASE_PRODUCTS_VIEWS, EMPTY_SEARCH_PHRASE_PRODUCTS_PAGE_VIEWS,
                                      PROJECTS_VIEWS_TITLE, SOLUTION_VIEWS_TITLE, SELLING_POINTS_VIEWS_TITLE,
                                      SEARCH_PROJECTS_VIEWS_TIP,
                                      EMPTY_SEARCH_PHRASE_PROJECTS_VIEWS, SEARCH_SOLUTIONS_VIEWS_TIP,
                                      SEARCH_SELLING_POINTS_VIEWS_TIP,
                                      BROCHURES_VIEWS_TITLE, SEARCH_BROCHURES_VIEWS_TIP,
                                      EMPTY_SEARCH_PHRASE_BROCHURES_VIEWS, SEARCH_ORDERS_VIEWS_TIP,
                                      EMPTY_SEARCH_PHRASE_SOLUTIONS_VIEWS, EMPTY_SEARCH_PHRASE_SELLING_POINTS_VIEWS,
                                      ORDERS_VIEWS_TITLE, EMPTY_SEARCH_PHRASE_ORDERS_VIEWS)
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import ManageProducts, ManageProductsPage, ManageProjects, \
    ManageSolution, ManageSellingPoints, ManageBrochures, ManageCarts


def get_count(query, flag_count):
    list_count = []
    for record in query:
        list_count.append(record[flag_count])
    return list_count


class ViewsReportsListView(ListView):
    model = ManageProducts
    template_name = "admin_panel/products_views.html"
    active_flag = 'products_views'
    searchManObj = SearchMan("ManageProducts")
    search_result = None
    report_man = ReportMan()
    title = PRODUCTS_VIEWS_TITLE

    def get_queryset(self):
        return ManageProducts.objects.values('product__name').annotate(num_users=Count('product__name')).order_by(
            '-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageProducts.objects.values('product__name').annotate(
                num_users=Count('product__name')).filter(
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
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageProducts, 'num_users'),
                'names': get_count(manageProducts, 'product__name'),
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
            manageProducts = ManageProducts.objects.values('product__name').annotate(
                num_users=Count('product__name')).order_by('num_users')
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

            'data_js': {
                "num_users": get_count(manageProducts, 'num_users'),
                'names': get_count(manageProducts, 'product__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PRODUCTS_VIEWS,
            }
        }
        return super().get(request)


class ProjectsViewsListView(ListView):
    model = ManageProjects
    template_name = "admin_panel/projects_views.html"
    active_flag = 'projects_views'
    searchManObj = SearchMan("ManageProjects")
    search_result = None
    report_man = ReportMan()
    title = PROJECTS_VIEWS_TITLE

    def get_queryset(self):
        return ManageProjects.objects.values('project__name').annotate(num_users=Count('project__name')).order_by(
            '-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageProjects.objects.values('project__name').annotate(
                num_users=Count('project__name')).filter(
                Q(project__name__icontains=search_message)).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Project Name')
            self.searchManObj.setSearchError(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProjects = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProjects = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProjects = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'projects_views_list': manageProjects,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_projects_views_tip': SEARCH_PROJECTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageProjects, 'num_users'),
                'names': get_count(manageProjects, 'project__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PROJECTS_VIEWS,
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
            manageProjects = ManageProjects.objects.values('project__name').annotate(
                num_users=Count('project__name')).order_by('num_users')
            self.searchManObj.setPaginator(manageProjects)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageProjects = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageProjects = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageProjects = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'projects_views_list': manageProjects,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_projects_views_tip': SEARCH_PROJECTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,

            'data_js': {
                "num_users": get_count(manageProjects, 'num_users'),
                'names': get_count(manageProjects, 'project__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PROJECTS_VIEWS,
            }
        }
        return super().get(request)

class SolutionsViewsListView(ListView):
    model = ManageSolution
    template_name = "admin_panel/solutions_views.html"
    active_flag = 'solutions_views'
    searchManObj = SearchMan("ManageSolutions")
    search_result = None
    report_man = ReportMan()
    title = SOLUTION_VIEWS_TITLE

    def get_queryset(self):
        return ManageSolution.objects.values('solution__title').annotate(num_users=Count('solution__title')).order_by(
            '-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageSolution.objects.values('solution__title').annotate(
                num_users=Count('solution__title')).filter(
                Q(solution__title__icontains=search_message)).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Solution Title')
            self.searchManObj.setSearchError(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageSolutions = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageSolutions = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageSolutions = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'solutions_views_list': manageSolutions,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_solutions_views_tip': SEARCH_SOLUTIONS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageSolutions, 'num_users'),
                'names': get_count(manageSolutions, 'solution__title'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_SOLUTIONS_VIEWS,
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
            manageSolutions = ManageSolution.objects.values('solution__title').annotate(
                num_users=Count('solution__title')).order_by('num_users')
            self.searchManObj.setPaginator(manageSolutions)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageSolutions = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageSolutions = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageSolutions = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'solutions_views_list': manageSolutions,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_solutions_views_tip': SEARCH_SOLUTIONS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,

            'data_js': {
                "num_users": get_count(manageSolutions, 'num_users'),
                'names': get_count(manageSolutions, 'solution__title'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_SOLUTIONS_VIEWS,
            }
        }
        return super().get(request)

class SellingPointsViewsListView(ListView):
    model = ManageSellingPoints
    template_name = "admin_panel/selling_points_views.html"
    active_flag = 'points_views'
    searchManObj = SearchMan("ManageSellingPoints")
    search_result = None
    report_man = ReportMan()
    title = SELLING_POINTS_VIEWS_TITLE

    def get_queryset(self):
        return ManageSellingPoints.objects.values('selling_point__name').annotate(num_users=Count('selling_point__name')).order_by(
            '-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageSellingPoints.objects.values('selling_point__name').annotate(
                num_users=Count('solution__title')).filter(
                Q(selling_point__name__icontains=search_message)).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Selling Point Name')
            self.searchManObj.setSearchError(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageSellingPoints = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageSellingPoints = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageSellingPoints = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'selling_points_views_list': manageSellingPoints,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_selling_points_views_tip': SEARCH_SELLING_POINTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageSellingPoints, 'num_users'),
                'names': get_count(manageSellingPoints, 'selling_point__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_SELLING_POINTS_VIEWS,
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
            manageSellingPoints = ManageSellingPoints.objects.values('selling_point__name').annotate(
                num_users=Count('selling_point__name')).order_by('num_users')
            self.searchManObj.setPaginator(manageSellingPoints)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageSellingPoints = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageSellingPoints = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageSellingPoints = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'selling_points_views_list': manageSellingPoints,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_selling_points_views_tip': SEARCH_SELLING_POINTS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageSellingPoints, 'num_users'),
                'names': get_count(manageSellingPoints, 'selling_point__name'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_SELLING_POINTS_VIEWS,
            }
        }
        return super().get(request)

class BrochuresViewsListView(ListView):
    model = ManageBrochures
    template_name = "admin_panel/brochures_views.html"
    active_flag = 'brochures_views'
    searchManObj = SearchMan("ManageBrochures")
    search_result = None
    report_man = ReportMan()
    title = BROCHURES_VIEWS_TITLE

    def get_queryset(self):
        return ManageBrochures.objects.values('brochures__title').annotate(num_users=Count('brochures__title')).order_by(
            '-num_users')

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
        if request.GET.get('search_phrase') != '':
            search_message = request.POST.get('search_phrase')
            self.search_result = ManageSellingPoints.objects.values('brochures__title').annotate(
                num_users=Count('brochures__title')).filter(
                Q(brochures__title__icontains=search_message)).order_by('-num_users')
            self.searchManObj.setPaginator(self.search_result)
            self.searchManObj.setSearchPhrase(search_message)
            self.searchManObj.setSearchOption('Brochures Title')
            self.searchManObj.setSearchError(False)

        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageBrochures = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageBrochures = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageBrochures = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'brochures_views_list': manageBrochures,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_brochures_views_tip': SEARCH_BROCHURES_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageBrochures, 'num_users'),
                'names': get_count(manageBrochures, 'brochures__title'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_BROCHURES_VIEWS,
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
            manageBrochures = ManageBrochures.objects.values('brochures__title').annotate(
                num_users=Count('brochures__title')).order_by('num_users')
            self.searchManObj.setPaginator(manageBrochures)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageBrochures = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageBrochures = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageBrochures = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'brochures_views_list': manageBrochures,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_brochures_views_tip': SEARCH_BROCHURES_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                "num_users": get_count(manageBrochures, 'num_users'),
                'names': get_count(manageBrochures, 'brochures__title'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_BROCHURES_VIEWS,
            }
        }
        return super().get(request)

class OrdersViewsListView(ListView):
    model = ManageCarts
    template_name = "admin_panel/orders_views.html"
    active_flag = 'orders_views'
    searchManObj = SearchMan("ManageOrders")
    search_result = None
    report_man = ReportMan()
    title = ORDERS_VIEWS_TITLE

    def get_queryset(self):
        return ManageCarts.objects.values('is_order_placed').annotate(num_orders=Count('order'))

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
            if request.POST.get('search_options') == 'uncompleted_orders':
                self.search_result = ManageCarts.objects.filter(is_order_placed=False).values('is_order_placed').annotate(num_orders=Count('order')).order_by('-id')
                self.searchManObj.setPaginator(self.search_result)
                self.searchManObj.setSearchPhrase("Uncompleted Orders")
                self.searchManObj.setSearchOption('Orders Status')
                self.searchManObj.setSearchError(False)
            if request.POST.get('search_options') == 'placed_orders':
                self.search_result = ManageCarts.objects.filter(is_order_placed=True).values(
                    'is_order_placed').annotate(num_orders=Count('order')).order_by('-id')
                self.searchManObj.setPaginator(self.search_result)
                self.searchManObj.setSearchPhrase("Placed Orders")
                self.searchManObj.setSearchOption('Orders Status')
                self.searchManObj.setSearchError(False)


        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageOrders = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageOrders = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageOrders = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'orders_views_list': manageOrders,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_orders_views_tip': SEARCH_ORDERS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                # "num_users": get_count(manageOrders, 'user'),
                # 'names': get_count(manageOrders, '__slug'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_ORDERS_VIEWS,
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
            manageOrders = ManageCarts.objects.values('is_order_placed').annotate(num_orders=Count('order'))
            self.searchManObj.setPaginator(manageOrders)
            self.searchManObj.setSearch(False)
        if request.GET.get('page'):
            # Grab the current page from query parameter consultant
            page = int(request.GET.get('page'))
        else:
            page = None

        try:
            paginator = self.searchManObj.getPaginator()
            manageOrders = paginator.page(page)
            # Create a page object for the current page.
        except PageNotAnInteger:
            # If the query parameter is empty then grab the first page.
            manageOrders = paginator.page(1)
            page = 1
        except EmptyPage:
            # If the query parameter is greater than num_pages then grab the last page.
            manageOrders = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        self.extra_context = {
            'reports': 'active',
            self.active_flag: 'active',
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
            'orders_views_list': manageOrders,
            'search': self.searchManObj.getSearch(),
            'search_result': self.search_result,
            'search_phrase': self.searchManObj.getSearchPhrase(),
            'search_option': self.searchManObj.getSearchOption(),
            'search_error': self.searchManObj.getSearchError(),
            'clear_search_tip': CLEAR_SEARCH_TIP,
            'search_orders_views_tip': SEARCH_ORDERS_VIEWS_TIP,
            'current_page': page,
            'title': self.title,
            'data_js': {
                # "num_users": get_count(manageOrders, 'user'),
                # 'names': get_count(manageOrders, 'order__slug'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_ORDERS_VIEWS,
            }
        }
        return super().get(request)

class ProductsPageViews(ListView):
    # import datetime
    # ManageProductsPage.objects.filter(
    #     visit_date__range=(datetime.datetime(2021, 1, 10, 11, 49, 25, 389820, tzinfo=datetime.timezone.utc),
    #     datetime.datetime(2022, 2, 20, 11, 49, 25, 389820, tzinfo=datetime.timezone.utc)))
    model = ManageProductsPage
    template_name = "admin_panel/product_page_views.html"
    active_flag = 'products_page_views'
    searchManObj = SearchMan("ManageProductsPage")
    search_result = None
    report_man = ReportMan()
    title = PRODUCTS_PAGE_VIEWS_TITLE

    def get_queryset(self):
        return ManageProductsPage.objects.values('visit_date').annotate(num_users=Count('user')).order_by('-num_users')

    # ManageProductsPage.objects.values('visit_date').filter(visit_date__year=2022).annotate(num_users=Count('user'))

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        if 'clear' not in request.POST:
            self.searchManObj.setSearch(True)
            print(request.POST.get('search_options'))
            print(request.POST.get('search_phrase_date'))
            if request.POST.get('search_options') == 'date':
                search_message = request.POST.get('search_phrase_date')
                self.search_result = ManageProductsPage.objects.values('visit_date').annotate(
                    num_users=Count('user')).filter(
                    Q(visit_date=search_message)).order_by('-num_users')
                self.searchManObj.setPaginator(self.search_result)
                self.searchManObj.setSearchPhrase(search_message)
                self.searchManObj.setSearchOption('Visiting Date')
                self.searchManObj.setSearchError(False)

            if request.POST.get('search_options') == 'month':
                search_message = request.POST.get('search_phrase_month')
                self.search_result = ManageProductsPage.objects.values('visit_date').annotate(
                    num_users=Count('user')).filter(
                    Q(visit_date__month=search_message)).order_by('-num_users')
                self.searchManObj.setPaginator(self.search_result)
                self.searchManObj.setSearchPhrase(search_message)
                self.searchManObj.setSearchOption('Visiting Month')
                self.searchManObj.setSearchError(False)

            if request.POST.get('search_options') == 'year':
                search_message = request.POST.get('search_phrase_year')
                self.search_result = ManageProductsPage.objects.values('visit_date').annotate(
                    num_users=Count('user')).filter(
                    Q(visit_date__year=search_message)).order_by('-num_users')
                self.searchManObj.setPaginator(self.search_result)
                self.searchManObj.setSearchPhrase(search_message)
                self.searchManObj.setSearchOption('Visiting Year')
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
            'title': self.title,

            'data_js': {
                "num_users": get_count(manageProductsPage, 'num_users'),
                'names': get_count(manageProductsPage, 'visit_date'),
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
                "num_users": get_count(manageProductsPage, 'num_users'),
                'names': get_count(manageProductsPage, 'visit_date'),
                "empty_search_phrase": EMPTY_SEARCH_PHRASE_PRODUCTS_PAGE_VIEWS,
            }
        }
        return super().get(request)
