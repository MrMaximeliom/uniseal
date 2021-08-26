import tempfile

from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from Util.permissions import UnisealPermission
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.shortcuts import redirect
from Util.utils import  SearchMan,createExelFile,ReportMan,delete_temp_folder


# Create your views here.
from Util.utils import rand_slug


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' data by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":11,
     "name": "product_name",
     "image": "product_image_url",
     "product_file":"product_file_url",
     "description":"Product_description",
     "added_date":"added_date"
     "category":category_id,
     "supplier":"supplier_id",
     }
     Use other functions by accessing this url:
     product/modifyProduct/<product's_id>
     Format of data will be as the previous data format for GET function
     To Get Products By Category use this url:
     product/modifyProduct/?category=<category_id>
     To Get Products By Supplier use this url:
     product/modifyProduct/?supplier=<supplier_id>
     To Get Products By Both Category and Supplier use this url:
     product/modifyProduct/?category=<category_id>&supplier=<supplier_id>

    """

    def get_view_name(self):
        return _("Create/Modify Products' Data")

    # def get_queryset(self):
    #     from .models import Product
    #     # returning default result if anything goes wrong
    #     queryset = Product.objects.all().order_by("id")
    #     return queryset

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer
    from .models import Product
    permission_classes = [UnisealPermission]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'supplier']


class ProductImagesViewSet(viewsets.ModelViewSet):
    """API endpoint to add or modify products' images by admin
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":10,
     "image": "product_image_url",
     "product":product_id
     }
     Use other functions by accessing this url:
     product/productImage/<productImage's_id>
     Format of data will be as the previous data format for GET function
     To Get All Product's Images for one product use this url:
     product/productImage/?product=<product_id>
    """

    def get_view_name(self):
        return _("Create/Modify Products Images")

    from .serializers import ProductImageSerializer
    serializer_class = ProductImageSerializer
    from .models import ProductImages
    permission_classes = [UnisealPermission]
    queryset = ProductImages.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


# class ProductVideoViewSet(viewsets.ModelViewSet):
#     """API endpoint to add or modify products' videos by admin
#         this endpoint allows GET,PUT,PATCH,DELETE functions
#         permissions to this view is restricted as the following:
#         - Only admin users can use all functions on this endpoint
#         - Registered users are only allowed to use GET function
#         Data will be retrieved in the following format for GET function:
#         {
#          "id":id,
#          "video": "product_video_url",
#          "product":product_id
#          }
#          Use other functions by accessing this url:
#          product/productVideo/<productVideo's_id>
#          Format of data will be as the previous data format for GET function
#          To Get All Product's Videos for one product use this url:
#          product/productVideo/?product=<product_id>
#         """
#
#     def get_view_name(self):
#         return _("Create/Modify Products Videos")
#
#     from .serializers import ProductVideoSerializer
#     serializer_class = ProductVideoSerializer
#     from .models import ProductVideos
#     permission_classes = [UnisealPermission]
#     queryset = ProductVideos.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['product']


class SimilarProductViewSet(viewsets.ModelViewSet):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Link/Unlink Similar Products")

    from .serializers import SimilarProductSerializer
    serializer_class = SimilarProductSerializer
    from .models import SimilarProduct
    permission_classes = [UnisealPermission]
    queryset = SimilarProduct.objects.all()


class FetchProductsByCategoryViewSet(generics.ListAPIView):
    """API endpoint to allow the admin to link or unlink similar products together
    this endpoint allows GET,PUT,PATCH,DELETE functions
    permissions to this view is restricted as the following:
    - Only admin users can use all functions on this endpoint
    - Registered users are only allowed to use GET function
    Data will be retrieved in the following format for GET function:
    {
     "id":9,
     "original_product": product_id,
     "similar_product":product_id
     }
     Use other functions by accessing this url:
     product/similarProducts/<similar_products's_id>
     Format of data will be as the previous data format for GET function
    """

    def get_view_name(self):
        return _("Fetch Products By Category")

    from .serializers import ProductSerializer
    serializer_class = ProductSerializer

    permission_classes = [UnisealPermission]

    from .models import Product
    queryset = Product.objects.all()

    # original get_queryset
    def get_queryset(self):
        from .models import Product
        # returning default result if anything goes wrong
        queryset = Product.objects.all()
        # category = self.request.query_params.get('category_id')
        category = self.kwargs['category_id']
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


from django.contrib.auth.decorators import login_required
def prepare_selected_query(selected_pages,paginator_obj,headers=None):
    product_name = []
    description = []
    added_date = []
    category = []
    supplier = []
    if headers is not None:
        headers_here = headers
        for header in headers_here:
            if header == "Product Name":
                for page in selected_pages:
                    for product in paginator_obj.page(page):
                        product_name.append(product.name)
            elif header == "Description":
                print("here in description")
                for page in selected_pages:
                    for product in paginator_obj.page(page):
                        description.append(product.description)
            elif header == "Category":
                for page in selected_pages:
                    for product in paginator_obj.page(page):
                        category.append(product.category.name)
            elif header == "Supplier":
                print("here in supplier selected")
                for page in selected_pages:
                    for product in paginator_obj.page(page):
                        supplier.append(product.supplier.name)
            elif header == "Added Date":
                for page in selected_pages:
                    for product in paginator_obj.page(page):
                        added_date.append(product.added_date.strftime('%d-%m-%y'))
    else:
        headers_here = ["Product Name", "Category", "Supplier", "Description", "Added Date"]
        for page in range(1, paginator_obj.num_pages):
            for product in paginator_obj.page(page):
                product_name.append(product.name)
                category.append(product.category.name)
                supplier.append(product.supplier.name)
                description.append(product.description)
                added_date.append(product.added_date.strftime('%d-%m-%y'))
    return headers_here, product_name, category, supplier, description, added_date

def prepare_query(paginator_obj,headers=None):
    product_name = []
    category = []
    supplier = []
    description = []
    added_date = []
    if headers is not None:
        print("now in headers is not none for prepare query")
        headers_here = headers
        for header in headers_here:
            if header == "Product Name":
                for page in range(1, paginator_obj.num_pages):
                    for product in paginator_obj.page(page):
                        product_name.append(product.name)
            elif header == "Category":
                for page in range(1, paginator_obj.num_pages):
                    for product in paginator_obj.page(page):
                        category.append(product.category.name)
            elif header == "Supplier":
                print("here in supplier")
                for page in range(1, paginator_obj.num_pages):
                    for product in paginator_obj.page(page):
                        supplier.append(product.supplier.name)
            elif header == "Description":
                print("here in description")
                for page in range(1, paginator_obj.num_pages):
                    for product in paginator_obj.page(page):
                        description.append(product.description)
            elif header == "Last Login":
                for page in range(1, paginator_obj.num_pages):
                    for product in paginator_obj.page(page):
                        added_date.append(product.added_date.strftime('%d-%m-%y'))
    else:
        headers_here = ["Product Name","Category","Supplier","Description","Added Date"]
        for page in range(1, paginator_obj.num_pages):
            for product in paginator_obj.page(page):
                product_name.append(product.name)
                category.append(product.category.name)
                supplier.append(product.supplier.name)
                description.append(product.description)
                added_date.append(product.added_date.strftime('%d-%m-%y'))

    # later for extracting actual data


    return headers_here,product_name,category,supplier,description,added_date
searchManObj = SearchMan("Product")
report_man = ReportMan()
report_man.setTempDir(tempfile.mkdtemp())



print("report man temp dir is: ",report_man.tempDir)
@login_required(login_url='login')
def all_products(request):
    from product.models import Product
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
    PRODUCT_NAME_SYNTAX_ERROR,
    CATEGORY_NAME_SYNTAX_ERROR,
    SUPPLIER_NAME_SYNTAX_ERROR

    )
    all_products = Product.objects.all().order_by("id")
    paginator = Paginator(all_products, 5)
    search_result = ''
    if 'temp_dir' in request.session and request.method == "GET":
        # deleting temp dir in GET requests
        if request.session['temp_dir'] != '':
            delete_temp_folder(request.session['temp_dir'])
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST :
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = Product.objects.filter(name=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Product.objects.filter(category__name=search_phrase).order_by("id")
            print("search results ",search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ',search_phrase)
            search_result = Product.objects.filter(supplier__name=search_phrase).order_by("id")
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
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('createExcel') == 'done':
        headers = []
        headers.append("Product Name") if request.POST.get('product_header') is not None else ''
        headers.append("Category") if request.POST.get('category_header') is not None else ''
        headers.append("Supplier") if request.POST.get('supplier_header') is not None else ''
        headers.append("Description") if request.POST.get('description_header') is not None else ''
        headers.append("Added Date") if request.POST.get('added_date_header') is not None else ''
        # create report functionality
        # setting all data as default behaviour
        if request.POST.get('pages_collector') != 'none':
            # get requested pages from the paginator of original page
            selected_pages = []
            query = searchManObj.getPaginator()
            print("original values: ", request.POST.get('pages_collector'))
            for item in request.POST.get('pages_collector'):
                if item != ",":
                    selected_pages.append(item)
            if len(headers) > 0:
                constructor = {}
                headers, product_name, category, supplier, description, added_date = prepare_selected_query(
                    selected_pages=selected_pages, paginator_obj=query,
                    headers=headers)
                if len(product_name) > 0:
                    constructor.update({"product_name": product_name})
                if len(category) > 0:
                    constructor.update({"category": category})
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(added_date) > 0:
                    constructor.update({"added_date": added_date})
                status, report_man.filePath, report_man.fileName = createExelFile(report_man, 'Report_For_Products',
                                                                                  headers, **constructor)
                if status:
                    messages.success(request, f"Report Successfully Created ")
                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")


            else:
                headers, product_name, category, supplier, description, added_date = prepare_selected_query(
                    selected_pages, query, headers)
                status, report_man.filePath, report_man.fileName = createExelFile(report_man, 'Report_For_Users',
                                                                                  headers, product_name=product_name,
                                                                                  category=category,
                                                                                  suppplier=supplier,
                                                                                  description=description,
                                                                                  added_date=added_date)
                if status:
                    messages.success(request, f"Report Successfully Created ")
                    # return redirect('download_file',filepath=filepath,filename=filename)

                    return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))

                else:
                    messages.error(request, "Sorry Report Failed To Create , Please Try Again!")
            # get the original query of page and then structure the data
        else:
            query = searchManObj.getPaginator()
            if len(headers) > 0:
                constructor = {}
                headers, product_name, category, supplier, description, added_date = prepare_query(query,
                                                                                                     headers=headers)
                if len(product_name) > 0:
                    constructor.update({"product_name": product_name})
                if len(category) > 0:
                    constructor.update({"category": category})
                if len(supplier) > 0:
                    constructor.update({"supplier": supplier})
                if len(description) > 0:
                    constructor.update({"description": description})
                if len(added_date) > 0:
                    constructor.update({"added_date": added_date})
                status, report_man.filePath, report_man.fileName = createExelFile(report_man, 'Report_For_Products',
                                                                                  headers, **constructor)
                if status:
                   request.session['temp_dir'] = report_man.tempDir
                   messages.success(request, f"Report Successfully Created ")
                   # return redirect('download_file',filepath=filepath,filename=filename)

                   return redirect('downloadReport', str(report_man.filePath), str(report_man.fileName))
                else:
                   messages.error(request, "Sorry Report Failed To Create , Please Try Again!")

            else:
                headers, product_name, category, supplier, description, added_date = prepare_query(query)
                status, report_man.filePath, report_man.fileName = createExelFile(report_man, 'Report_For_Products',
                                                                                  headers, product_name=product_name,
                                                                                  category=category,
                                                                                  supplier=supplier,
                                                                                  description=description,
                                                                                  added_date=added_date)
                if status:
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
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'product/all_products.html',
                  {
                      'title': _('All Products'),
                      'all_products': 'active',
                      'all_products_data': products,
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
                          "product_error": PRODUCT_NAME_SYNTAX_ERROR,
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )


@login_required(login_url='login')
def add_products(request):
    from .forms import ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product.slug = slugify(rand_slug())
            product.save()
            product_name = form.cleaned_data.get('name')

        else:
            print('there was an error dude!')
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = ProductForm()
    context = {
        'title': _('Add Products'),
        'add_products': 'active',
        'all_products': all_products,
        'form': form,
        # 'all_categories': all_categories,
        # 'all_suppliers': all_suppliers,
    }
    return render(request, 'product/add_products.html', context)


@login_required(login_url='login')
def delete_products(request):
    from product.models import Product
    all_products = Product.objects.all().order_by('id')
    paginator = Paginator(all_products, 5)
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR

    )
    search_result = ''
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = Product.objects.filter(name=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Product.objects.filter(category__name=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = Product.objects.filter(supplier__name=search_phrase).order_by("id")
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
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {
        'title': _('Delete Products'),
        'delete_products': 'active',
        'all_products': all_products,
        'all_products_data': products,
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
            "product_error": PRODUCT_NAME_SYNTAX_ERROR,
            "category_error": CATEGORY_NAME_SYNTAX_ERROR,
            "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
        }
    }
    return render(request, 'product/delete_products.html', context)


@login_required(login_url='login')
def edit_product(request, slug):
    from product.models import Product
    from .forms import ProductForm, ProductImagesForm
    all_products = Product.objects.all()

    # fetch the object related to passed id
    obj = get_object_or_404(Product, slug=slug)

    # pass the object as instance in form
    product_form = ProductForm(request.POST or None, instance=obj)
    # product_image_form = ProductImagesForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if product_form.is_valid():
        product_form.save()
        product_name = product_form.cleaned_data.get('name')
        messages.success(request, f"Successfully Updated : {product_name} Data")
    else:
        for field, items in product_form.errors.items():
            for item in items:
                messages.error(request, '{}: {}'.format(field, item))
        # product_image_form.save()
    context = {
        'title': _('Edit Products'),
        'edit_products': 'active',
        'all_products': all_products,
        'product_form': product_form,
        'product': obj,
        # 'product_image_form': product_image_form
    }
    return render(request, 'product/edit_product.html', context)


@login_required(login_url='login')
def edit_products(request):
    from product.models import Product
    from Util.search_form_strings import (
        EMPTY_SEARCH_PHRASE,
        PRODUCT_NAME_SYNTAX_ERROR,
        CATEGORY_NAME_SYNTAX_ERROR,
        SUPPLIER_NAME_SYNTAX_ERROR

    )
    search_result = ''
    all_products = Product.objects.all().order_by("id")
    paginator = Paginator(all_products, 5)
    if request.method == "POST" and 'clear' not in request.POST and 'createExcel' not in request.POST:
        searchManObj.setSearch(True)
        if request.POST.get('search_options') == 'product':
            print('here now in product search')
            search_message = request.POST.get('search_phrase')
            search_result = Product.objects.filter(name=search_message).order_by('id')
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_message)
            searchManObj.setSearchOption('Product Name')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'category':
            print('here now in category search')
            search_phrase = request.POST.get('search_phrase')
            search_result = Product.objects.filter(category__name=search_phrase).order_by("id")
            print("search results ", search_result)
            searchManObj.setPaginator(search_result)
            searchManObj.setSearchPhrase(search_phrase)
            searchManObj.setSearchOption('Category')
            searchManObj.setSearchError(False)
        elif request.POST.get('search_options') == 'supplier':
            print('here now in supplier search')
            search_phrase = request.POST.get('search_phrase')
            print('search phrase is ', search_phrase)
            search_result = Product.objects.filter(supplier__name=search_phrase).order_by("id")
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
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.method == "POST" and request.POST.get('clear') == 'clear':
        all_products = Product.objects.all().order_by("id")
        searchManObj.setPaginator(all_products)
        searchManObj.setSearch(False)
    if request.GET.get('page'):
        # Grab the current page from query parameter
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        paginator = searchManObj.getPaginator()
        products = paginator.page(page)
        # Create a page object for the current page.
    except PageNotAnInteger:
        # If the query parameter is empty then grab the first page.
        products = paginator.page(1)
        page = 1
    except EmptyPage:
        # If the query parameter is greater than num_pages then grab the last page.
        products = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'product/edit_products.html',
                  {
                      'title': _('Edit Products'),
                      'edit_products': 'active',
                      'all_products_data': products,
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
                          "product_error": PRODUCT_NAME_SYNTAX_ERROR,
                          "category_error": CATEGORY_NAME_SYNTAX_ERROR,
                          "supplier_error": SUPPLIER_NAME_SYNTAX_ERROR,
                      }
                  }
                  )


@login_required(login_url='login')
def product_details(request, slug):
    from product.models import Product, ProductImages
    # from .forms import ProductForm
    # all_products = Product.objects.all().order_by("id")
    # paginator = Paginator(all_products, 5)
    # fetch the object related to passed id
    product = get_object_or_404(Product, slug=slug)
    productImages = ProductImages.objects.filter(product__slug=slug)
    pureImages = list()
    if productImages:
        pureImages.append(product.image.url)
        for image in productImages:
            pureImages.append(image.image.url)

    if request.method == "GET":
        if productImages:
            print("its noot empty yo!")
            print(product.image.url)
        else:
            print("its emmpty yoooo!")

    return render(request, 'product/product_detail.html',
                  {
                      'title': _('Product Details'),
                      'all_products': 'active',
                      'product_data': product,
                      'product_images': pureImages,
                      'product_original_image': product.image.url

                  }
                  )


@login_required(login_url='login')
def product_images(request, slug):
    from product.models import Product, ProductImages
    from .forms import ProductImagesForm
    # all_products = Product.objects.all().order_by("id")
    # paginator = Paginator(all_products, 5)
    # fetch the object related to passed id
    product = get_object_or_404(Product, slug=slug)
    productImages = ProductImages.objects.filter(product__slug=slug)
    pureImages = list()
    if productImages:
        pureImages.append(product.image.url)
        for image in productImages:
            pureImages.append(image.image.url)

    if request.method == 'POST':
        form = ProductImagesForm(request.POST)
        if form.is_valid():
            form.save()
            # country_name = form.cleaned_data.get('name')
            # messages.success(request, f"New Product Image Added: {country_name}")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = ProductImagesForm()

    return render(request, 'product/product_images.html',
                  {
                      'title': _('Product Images'),
                      'all_products': 'active',
                      'product_data': product,
                      'product_images': pureImages,
                      'product_original_image': product.image.url,
                      'form': form

                  }
                  )


def confirm_delete(request, id):
    from product.models import Product
    obj = get_object_or_404(Product, id=id)
    try:
        obj.delete()
        messages.success(request, f"Product {obj.name} deleted successfully")
    except:
        messages.error(request, f"Product {obj.name} was not deleted , please try again!")

    return redirect('deleteProducts')
