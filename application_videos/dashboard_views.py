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
@staff_member_required(login_url='login')
def all_videos(request):
    from .models import ProductApplicationVideos
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR,
        PRODUCT_NOT_FOUND,
        CLEAR_SEARCH_TIP,
        SEARCH_PRODUCTS_TIP,
    )
    all_videos = ProductApplicationVideos.objects.all().order_by("id")
    paginator = Paginator(all_videos, 5)
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        print("delete reports")
        if request.session['temp_dir'] != '':
            delete_temp_folder()
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            search_message = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__name__icontains=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__category__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = ProductApplicationVideos.objects.filter(product__supplier__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Supplier')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        videos = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        videos = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        videos = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'application_videos/all_videos.html',
                  {
                      'title': _('Products Application Videos'),
                      'videos':'active',
                      'all_videos': 'active',
                      'all_products_data': videos,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),
                      'clear_search_tip': CLEAR_SEARCH_TIP,
                      'search_products_tip': SEARCH_PRODUCTS_TIP,
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "product_error": PRODUCT_NAME_SYNTAX_ERROR,
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      },
                      'not_found': PRODUCT_NOT_FOUND,
                  }
                  )
@staff_member_required(login_url='login')
def product_videos(request, slug=None):
    from .models import ProductApplicationVideos
    from product.models import Product
    allProducts = Product.objects.all()
    context = {
        'title': _('Add Videos'),
        'add_videos': 'active',
        'allProducts': allProducts,
        'videos': 'active',
    }
    if slug != None and request.method == 'GET':
        try:
            selected_product = get_object_or_404(Product,slug=slug)
        except Product.DoesNotExist:
            raise Http404("Given query not found....")
        product_videos = ProductApplicationVideos.objects.filter(product__slug=slug)
        print("product videos is: ",product_videos)
        context.update({
            'product_videos': product_videos,
            'slug': slug,
            'selected_product':selected_product.name,
        })
    if request.method == 'POST' and 'search_product' in request.POST:
        if request.POST.get('search_options') != 'none':
            print('searching for product videos')
            chosen_project = request.POST.get('search_options')
            # print("chosen one is: ",chosen_project.len())
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
                ProductApplicationVideos(product=selected_product,application_video=video)
            )
        ProductApplicationVideos.objects.bulk_create(added_videos)
        print("length of selected videos ",len(selected_videos))
        print("selected videos are: \n",selected_videos)
        messages.success(request, _("Videos added successfully!"))

        return redirect('productVideos', slug=slug)

    return render(request, 'application_videos/add_videos.html',
                  context

                  )
@staff_member_required(login_url='login')
def delete_products_videos(request):
    from application_videos.models import ProductApplicationVideos
    # from product.models import Product
    all_videos = ProductApplicationVideos.objects.all().order_by('id')
    paginator = Paginator(all_videos, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR,
        PRODUCT_NOT_FOUND,
        CLEAR_SEARCH_TIP,
        SEARCH_PRODUCTS_TIP,
    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__name__icontains=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__category__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = ProductApplicationVideos.objects.filter(product__supplier__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Supplier')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET:
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear' and not searchManObj.getSearch():
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        videos = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        videos = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        videos = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {
        'title': _('Delete Products Videos'),
        'delete_videos': 'active',
        'all_videos': all_videos,
        'all_videos_data': videos,
        'page_range': paginator.page_range,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'search': searchManObj.getSearch(),
        'search_result': search_result,
        'search_phrase': searchManObj.getSearchPhrase(),
        'search_option': searchManObj.getSearchOption(),
        'search_error': searchManObj.getSearchError(),
        'clear_search_tip': CLEAR_SEARCH_TIP,
        'search_products_tip': SEARCH_PRODUCTS_TIP,
        'products': 'active',
        'data_js': {
            "empty_search_phrase": EMPTY_SEARCH_PHRASE,
            "product_error": PRODUCT_NAME_SYNTAX_ERROR,
            "category_error": CATEGORY_NAME_SYNTAX_ERROR,
            "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
        },
        'not_found': PRODUCT_NOT_FOUND,
    }
    return render(request, 'application_videos/delete_videos.html', context)
@staff_member_required(login_url='login')
def confirm_delete(request, id):
    from application_videos.models import ProductApplicationVideos
    obj = get_object_or_404(ProductApplicationVideos, id=id)
    try:
        obj.delete()
        messages.success(request, f"Application video for Product << {obj.product.name} >> deleted successfully")
    except:
        messages.error(request, f"Application video for Product << {obj.product.name} >> was not deleted , please try again!")

    return redirect('deleteVideos')

@staff_member_required(login_url='login')
def edit_video(request, slug):
    from application_videos.models import ProductApplicationVideos
    from .forms import ApplicationVideoForm
    all_videos = ProductApplicationVideos.objects.all()

    # fetch the object related to passed id
    obj = get_object_or_404(ProductApplicationVideos, slug=slug)

    # pass the object as instance in form
    application_video_form = ApplicationVideoForm(request.POST or None, instance=obj)
    if application_video_form.is_valid():
        application_video_form.save()
        product_name = application_video_form.cleaned_data.get('product')
        messages.success(request, f"Successfully Updated : << {product_name} >> Data")
    else:
        for field, items in application_video_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))
        # product_image_form.save()
    context = {
        'title': _('Edit Products'),
        'edit_products': 'active',
        'all_videos': all_videos,
        'video_form': application_video_form,
        'video': obj,
        'videos': 'active',
    }
    return render(request, 'application_videos/edit_video.html', context)

@staff_member_required(login_url='login')
def edit_videos(request):
    from .models import ProductApplicationVideos
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR,
        PRODUCT_NOT_FOUND,
        CLEAR_SEARCH_TIP,
        SEARCH_PRODUCTS_TIP,

    )
    search_result = ''
    all_videos = ProductApplicationVideos.objects.all().order_by("id")
    paginator = Paginator(all_videos, 5)
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__name__icontains=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = ProductApplicationVideos.objects.filter(product__category__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = ProductApplicationVideos.objects.filter(product__supplier__name__icontains=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Supplier')
            searchManObj.setSearchError(False)
        else:
            messages.error(request,
                           "Please choose an item from list , then write search phrase to search by it!")
            searchManObj.setSearchError(True)
    if request.method == "GET" and 'page' not in request.GET and not searchManObj.getSearch():
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_videos = ProductApplicationVideos.objects.all().order_by("id")
        searchManObj.setPaginator(all_videos)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        videos = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        videos = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        videos = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'application_videos/edit_videos.html',
                  {
                      'title': _('Edit Videos'),
                      'edit_videos': 'active',
                      'videos': 'active',
                      'all_videos_data': videos,
                      'page_range': paginator.page_range,
                      'num_pages': paginator.num_pages,
                      'current_page': page,
                      'search': searchManObj.getSearch(),
                      'search_result': search_result,
                      'search_phrase': searchManObj.getSearchPhrase(),
                      'search_option': searchManObj.getSearchOption(),
                      'search_error': searchManObj.getSearchError(),

                      'clear_search_tip': CLEAR_SEARCH_TIP,
                      'search_products_tip': SEARCH_PRODUCTS_TIP,
                      'data_js': {
                          "empty_search_phrase": EMPTY_SEARCH_PHRASE,
                          "product_error": PRODUCT_NAME_SYNTAX_ERROR,
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      },
                      'not_found': PRODUCT_NOT_FOUND
                  }
                  )