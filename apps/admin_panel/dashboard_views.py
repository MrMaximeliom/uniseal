from django.views.generic import ListView
from Util.search_form_strings import (CLEAR_SEARCH_TIP ,
    PRODUCTS_VIEWS_TITLE,SEARCH_PRODUCTS_VIEWS_TIP)
from Util.utils import delete_temp_folder, SearchMan, ReportMan
from .models import ManageProducts
from django.db.models import Count
#     ManageProductsPage,ManageBrochures,ManageSellingPoints,ManageProjects,ManageCarts,ManageSolution
# from .forms import (ManageBrochuresForm,ManageProductsForm,
#                     ManageCartsForm,ManageProductsPageForm
# ,ManageProjectsForm,ManageSellingPointsForm,ManageSolutionForm)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#
#
# class ManageFormView(FormView):
#     template_name = 'offer/add_offers.html'
#     form_class = OfferForm
#     success_url = 'addOffers'
#
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, "Offer Added Successfully")
#         return super().form_valid(form)
#
#     extra_context = {
#         'offers': 'active',
#         'add_offers': 'active',
#         'title':ADD_OFFERS_TITLE
#     }


class ViewsReportsListView(ListView):
    model = ManageProducts
    template_name = "admin_panel/products_views.html"
    active_flag = 'products_views'
    searchManObj = SearchMan("Products")
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
        # search by username
        # ManageProducts.objects.values_list('product__name', 'user').annotate(num_users=Count('product__name')).filter(
        #     user__username='waleed')
        if request.POST.get('clear') == 'clear':
            manageProducts = self.get_queryset()
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
            'title':self.title,
            'data_js': {
                "num_users": self.get_count('num_users'),
                'products_names': self.get_count('product__name'),
            }
            # 'num_users':self.get_count('num_users'),
            # 'products_names': self.get_count('product__name'),

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
            manageProducts = ManageProducts.objects.values('product__name').annotate(num_users=Count('product__name'))
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
            }
        }
        return super().get(request)


