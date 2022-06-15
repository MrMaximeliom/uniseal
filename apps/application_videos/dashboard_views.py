from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _

from Util.utils import SearchMan, ReportMan, delete_temp_folder

# Create your views here.
searchManObj = SearchMan("ProductVideos")
report_man = ReportMan()
from apps.application_videos.models import ProductApplicationVideos
# new code starts here
from apps.common_code.views import BaseListView


class VideosListView(BaseListView):
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
        if request.POST.get('search_options') == 'product':
            search_message = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__name__icontains=search_message).order_by(
                'id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(
                product__category__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = ProductApplicationVideos.objects.filter(
                product__supplier__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Supplier')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
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

@staff_member_required(login_url='login')
def product_videos(request, slug=None):
    from .models import ProductApplicationVideos
    from apps.product.models import Product
    allProducts = Product.objects.all()
    context = {
        'title': _('Add Videos'),
        'add_videos': 'active',
        'allProducts': allProducts,
        'videos': 'active',
    }
    if slug != None and request.method == 'GET':
        try:
            selected_product = get_object_or_404(Product, slug=slug)
        except Product.DoesNotExist:
            raise Http404("Given query not found....")
        product_videos = ProductApplicationVideos.objects.filter(product__slug=slug)
        print("product videos is: ", product_videos)
        context.update({
            'product_videos': product_videos,
            'slug': slug,
            'selected_product': selected_product.name,
        })
    if request.method == 'POST' and 'search_product' in request.POST:
        if request.POST.get('search_options') != 'none':
            print('searching for product videos')
            chosen_project = request.POST.get('search_options')
            return redirect('productVideos', slug=chosen_project)
        else:
            messages.error(request, "Please choose a project from the list")

    if request.method == 'POST' and 'add_videos' in request.POST:
        print("here now")
        selected_product = Product.objects.get(slug=slug)
        added_videos = list()
        selected_videos = request.POST.getlist('video')
        for video in selected_videos:
            added_videos.append(
                ProductApplicationVideos(product=selected_product, application_video=video)
            )
        ProductApplicationVideos.objects.bulk_create(added_videos)
        messages.success(request, _("Videos added successfully!"))

        return redirect('productVideos', slug=slug)

    return render(request, 'application_videos/add_videos.html',
                  context

                  )

